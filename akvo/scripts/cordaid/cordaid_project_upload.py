# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import getopt
import sys

from lxml import etree

from tastypie.http import HttpCreated, HttpNoContent

from django.http import HttpResponse

from django.core.management import setup_environ
from akvo import settings
setup_environ(settings)

from akvo.scripts.cordaid import log, API_VERSION, CORDAID_IATI_ACTIVITIES_XML, CORDAID_UPLOAD_CSV_FILE, ACTION_CREATE_PROJECT, ERROR_EXCEPTION, ERROR_UPLOAD_ACTIVITY, ERROR_CREATE_ACTIVITY, ERROR_UPDATE_ACTIVITY, ACTION_UPDATE_PROJECT, CORDAID_ACTIVITIES_CSV_FILE, print_log, init_log, ERROR_MULTIPLE_OBJECTS, ERROR_NO_ORGS
from requester import Requester


class HttpNoContent(HttpResponse):
    status_code = 204

def post_an_activity(activity_element, user):
    try:
        iati_id = activity_element.findall('iati-identifier')[0].text
        project = Requester(
            method='post',
            url_template="http://{domain}/api/{api_version}/iati_activity/"
                "?format=xml&api_key={api_key}&username={username}",
            url_args=user,
            headers={'content-type': 'application/xml', 'encoding': 'utf-8'},
            data=etree.tostring(activity_element),
            accept_codes=[HttpCreated.status_code]
        )
    except Exception, e:
        return False, "{extra}", dict(
            iati_id = iati_id,
            event = ERROR_EXCEPTION,
            extra = e.message,
        )
    if project.response.text:
        return False,  "**** Error creating iati-activity: {iati_id}", dict(
            iati_id = iati_id,
            event = ERROR_CREATE_ACTIVITY,
            extra = project.response.text
        )
    elif project.response.status_code is HttpCreated.status_code:
        return True, "Created project for iati-activity: {iati_id}", dict(
            iati_id = iati_id, event = ACTION_CREATE_PROJECT
        )
    else:
        return (
            False,
            "**** Error creating iati-activity: {iati_id}. HTTP status code: {extra}", dict(
                iati_id = iati_id,
                event = ERROR_UPLOAD_ACTIVITY,
                extra = project.response.status_code,
            )
        )

# root[i].findall('iati-identifier')[0].text

def put_an_activity(activity_element, pk, url_args):
    "NOTE: does not work!!!"
    url_args.update(pk=pk)
    try:
        iati_id = activity_element.findall('iati-identifier')[0].text
        project = Requester(
            method='put',
            url_template="http://{domain}/api/{api_version}/iati_activity/{pk}/?"
                "format=xml&api_key={api_key}&username={username}",
            url_args=url_args,
            headers={'content-type': 'application/xml', 'encoding': 'utf-8'},
            data=etree.tostring(activity_element),
            accept_codes=[HttpNoContent.status_code]
        )
    except Exception, e:
        return False, "{extra}", dict(
            iati_id = iati_id,
            event = ERROR_EXCEPTION,
            extra = e.message
        )
    if project.response.text:
        return False, "**** Error creating iati-activity: {iati_id}", dict(
            iati_id = iati_id,
            event = ERROR_UPDATE_ACTIVITY,
            extra = project.response.text
        )
    elif project.response.status_code is HttpNoContent.status_code:
        return True, "Updated project for iati-activity: {iati_id} (Akvo pk: {pk})", dict(
            iati_id = iati_id,
            event = ACTION_UPDATE_PROJECT,
            pk = pk
        )
    else:
        return (
            False,
            "**** Error updating iati-activity: {iati_id}. HTTP status code: {extra}", dict(
                iati_id = iati_id,
                event = ERROR_UPLOAD_ACTIVITY,
                extra = project.response.status_code,
            )
        )

def usage(script_name):
    print(
        "\nUsage: %s <domain> <username> [options]\n\n"
        "  <domain>         The domain you are posting to, e.g. test.akvo.org\n"
        "  <username>       Your Akvo account username\n\n"
        "  Options (note that either PWD or KEY must be supplied):\n"
        "     -h, --help    show this message\n\n"
        "     -p PWD, --password=PWD\n"
        "       Supply your Akvo account password\n\n"
        "     -k KEY, --api_key=KEY\n"
        "       Supply the API key generated in your Akvo user profile\n"
        % script_name)

def api_user(domain, username, password='', api_key=''):
    user = dict(domain=domain, username=username, api_version=API_VERSION,)
    if api_key:
        user['api_key'] = api_key
        return user
    elif password:
        auth = Requester(
            method='post',
            url_template="http://{domain}/auth/token/",
            url_args=dict(domain=domain),
            data=dict(username=username, password=password),
        )
        xml = auth.response.text
        root = etree.fromstring(xml)
        user['api_key'] = root.find("api_key").text
        return user
    else:
        raise Exception("Either password or API key must be supplied")

def credentials_from_args(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "hp:k:", ["help", "password=", "api_key="])
    except getopt.GetoptError as e:
        print (str(e))
        usage(argv[0])
        sys.exit(2)
    kwargs = {}
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])
            sys.exit()
        # TODO: see if it's possible to suppress password echoing in terminal
        elif opt in ("-p", "--password"):
            kwargs['password'] = arg
        elif opt in ("-k", "--api_key"):
            kwargs['api_key'] = arg
    try:
        domain = args[0]
        username = args[1]
    except IndexError:
        usage(argv[0])
        sys.exit(2)
    try:
        user = api_user(domain, username, **kwargs)
        return user
    except Exception, e:
        print "{message}".format(message=e.message)
        usage(argv[0])
        return None

def get_project_count(user, **q_args):
    """
    query the API for projects associated with a given internal_id
    """
    url_args = user
    url_args.update(
        extra_args = "&".join(
            ["{}={}".format(item[0], item[1]) for item in q_args.items()]
        )
    )
    try:
        project = Requester(
            url_template="http://{domain}/api/{api_version}/project/?"
                "format=json&api_key={api_key}&username={username}&{extra_args}",
            url_args=url_args
        )
    except Exception, e:
        print "{message}".format(message=e.message)
        return False, None
    return True, project

def upload_activities(argv):
    user = credentials_from_args(argv)
    if user:
        with open(CORDAID_IATI_ACTIVITIES_XML, 'r') as f:
            root = etree.fromstring(f.read())
            AKVO_NS = '{{{akvo_ns}}}'.format(akvo_ns=root.nsmap['akvo'])
            activities = root.findall('iati-activity')
            activity_count = len(activities)
            for i in range(activity_count):
                internal_id = activities[i].get(AKVO_NS + 'internal-project-id')
                iati_id=activities[i].findall('iati-identifier')[0].text
                print "({current} of {activity_count}) Processing activity {iati_id}".format(current=i+1, activity_count=activity_count, iati_id=iati_id),
                if len(activities[i].findall('participating-org')) > 0:
                    if internal_id:
                        ok, project = get_project_count(user, **dict(partnerships__internal_id=internal_id))
                    elif iati_id:
                        ok, project = get_project_count(user, **dict(partnerships__iati_activity_id=iati_id))
                    if not ok:
                        continue #error msg already output
                    project_count = project.response.json()['meta']['total_count']
                    if project_count == 0:
                        ok, message, data = post_an_activity(activities[i], user)
                        log(message, data)
                        print message.format(**data)
                    elif project_count == 1:
                        pk = project.response.json()['objects'][0]['id']
                        ok, message, data = put_an_activity(activities[i], pk, user)
                        log(message, data)
                        print message.format(**data)
                    elif project_count > 1:
                        data = dict(iati_id=iati_id, event=ERROR_MULTIPLE_OBJECTS, extra=internal_id)
                        log(None, data)
                        print(
                            "**** Error updating iati-activity: {iati_id}. "
                                "More than one project with internal ID {extra} exists.".format(**data)
                        )
                else:
                    message = "Iati-activity {iati_id} has no participating-orgs, aborting"
                    data = dict(iati_id = iati_id, event = ERROR_NO_ORGS,)
                    log(message, data)
                    print(message.format(**data))

if __name__ == '__main__':
    upload_activities(sys.argv)
    log_file = init_log(CORDAID_UPLOAD_CSV_FILE)
    names = (u'iati_id', u'pk', u'event', u'extra')
    print_log(log_file, names)
