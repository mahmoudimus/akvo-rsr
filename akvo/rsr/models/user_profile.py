# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

import logging
logger = logging.getLogger('akvo.rsr')

from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from workflows import WorkflowBase
from permissions import PermissionBase
from permissions.models import Role

from akvo.gateway.models import GatewayNumber, Gateway
# from akvo.rsr.models import Organisation, ProjectUpdate, SmsReporter
from akvo.rsr.utils import (
    GROUP_RSR_EDITORS, GROUP_RSR_PARTNER_ADMINS, GROUP_RSR_PARTNER_EDITORS
)
from akvo.rsr.utils import (
    groups_from_user, who_am_i, send_now, state_equals
)


class UserProfileManager(models.Manager):
    def process_sms(self, mo_sms):
        try:
            profile = self.get(phone_number__exact=mo_sms.sender)  # ??? reporter instead ???
            #state = get_state(profile)
            #if state:
            if state_equals(profile, profile.STATE_PHONE_NUMBER_ADDED):
                logger.debug("%s: state is %s." % (who_am_i(), profile.STATE_PHONE_NUMBER_ADDED))
                # look for validation code
                if profile.validation == mo_sms.message.strip().upper():
                    profile.confirm_validation(mo_sms)
                else:
                    logger.error(
                        'Error in UserProfileManager.process_sms: "%s" is not the correct validation code expected "%s". Locals:\n %s\n\n' % (
                            mo_sms.message, profile.validation, locals()))
            #elif state_equals(profile, profile.STATE_PHONE_NUMBER_VALIDATED):
            #    # we shouldn't be here...phone ok, but no project selected :(
            #    logger.error('Error in UserProfileManager.process_sms: workflow in state "%s" meaning phone is validated, but no project has been selected. Locals:\n %s\n\n' % (profile.STATE_PHONE_NUMBER_VALIDATED, locals()))
            elif state_equals(profile, profile.STATE_UPDATES_ENABLED):
                logger.debug("%s: state is %s." % (who_am_i(), profile.STATE_UPDATES_ENABLED))
                # time to make an SMS update!
                try:
                    reporter = profile.reporters.get(gw_number=GatewayNumber.objects.get(number=mo_sms.receiver))
                    reporter.create_sms_update(mo_sms)
                except Exception, e:
                    logger.error(
                        "Error in UserProfileManager.process_sms: %s. Locals:\n %s\n\n" % (e.message, locals()))
            else:
                logger.error(
                    'Error in UserProfileManager.process_sms: workflow disabled or in an unknown state. Locals:\n %s\n\n' % (
                        locals()))
        except Exception, e:
            logger.exception('%s Locals:\n %s\n\n' % (e.message, locals(), ))


class UserProfile(models.Model, PermissionBase, WorkflowBase):
    '''
    Extra info about a user.
    '''
    user = models.OneToOneField(User)
    organisation = models.ForeignKey('Organisation')
    phone_number = models.CharField(max_length=50, blank=True)  # TODO: check uniqueness if non-empty
    validation = models.CharField(_('validation code'), max_length=20, blank=True)

    objects = UserProfileManager()

    # "constants" for use with SMS updating workflow
    VALIDATED = u'IS_VALID'  # _ in IS_VALID guarantees validation code will never be generated to equal VALIDATED
    WORKFLOW_SMS_UPDATE = u'SMS update'  # Name of workflow for SMS updating
    STATE_PHONE_NUMBER_ADDED = u'Phone number added'  # Phone number has been added to the profile
    #STATE_PHONE_NUMBER_VALIDATED = u'Phone number validated' #The phone has been validated with a validation code SMS
    STATE_UPDATES_ENABLED = u'Updates enabled'  # The phone is enabled, registered reporters will create updates on respective project
    STATE_PHONE_DISABLED = u'Phone disabled'  # The phone is disabled, preventing the processing of incoming SMSs
    TRANSITION_ADD_PHONE_NUMBER = u'Add phone number'
    TRANSITION_VALIDATE_PHONE_NUMBER = u'Validate phone number'
    TRANSITION_ENABLE_UPDATING = u'Enable updating'
    TRANSITION_DISABLE_UPDATING = u'Disable updating'
    GROUP_SMS_UPDATER = u'SMS updater'
    GROUP_SMS_MANAGER = u'SMS manager'
    ROLE_SMS_UPDATER = u'SMS updater'
    ROLE_SMS_MANAGER = u'SMS manager'
    PERMISSION_ADD_SMS_UPDATES = 'add_sms_updates'
    PERMISSION_MANAGE_SMS_UPDATES = 'manage_sms_updates'
    GATEWAY_42IT = '42it'

    class Meta:
        verbose_name = _(u'user profile')
        verbose_name_plural = _(u'user profiles')
        ordering = ['user__username', ]

    def __unicode__(self):
        return self.user.username

    def user_name(self):
        return self.__unicode__()

    def organisation_name(self):
        return self.organisation.name

    def updates(self):
        """
        return all updates created by the user
        """
        return get_model('rsr', 'ProjectUpdate').objects.filter(user=self.user).order_by('-time')

    def latest_update_date(self):
        updates = self.updates()
        if updates:
            return updates[0].time
        else:
            return None

    #methods that interact with the User model
    def get_is_active(self):
        return self.user.is_active

    get_is_active.boolean = True  # make pretty icons in the admin list view
    get_is_active.short_description = _(u'user is activated (may log in)')

    def set_is_active(self, set_it):
        self.user.is_active = set_it
        self.user.save()

    def get_is_staff(self):
        return self.user.is_staff

    get_is_staff.boolean = True  # make pretty icons in the admin list view

    def set_is_staff(self, set_it):
        self.user.is_staff = set_it
        self.user.save()

    def get_is_rsr_admin(self):
        return GROUP_RSR_EDITORS in groups_from_user(self.user)

    def get_is_org_admin(self):
        return GROUP_RSR_PARTNER_ADMINS in groups_from_user(self.user)

    get_is_org_admin.boolean = True  # make pretty icons in the admin list view
    get_is_org_admin.short_description = _(u'user is an organisation administrator')

    def set_is_org_admin(self, set_it):
        if set_it:
            self._add_user_to_group(GROUP_RSR_PARTNER_ADMINS)
        else:
            self._remove_user_from_group(GROUP_RSR_PARTNER_ADMINS)

    def get_is_org_editor(self):
        return GROUP_RSR_PARTNER_EDITORS in groups_from_user(self.user)

    get_is_org_editor.boolean = True  # make pretty icons in the admin list view
    get_is_org_editor.short_description = _(u'user is a project editor')

    def set_is_org_editor(self, set_it):
        if set_it:
            self._add_user_to_group(GROUP_RSR_PARTNER_EDITORS)
        else:
            self._remove_user_from_group(GROUP_RSR_PARTNER_EDITORS)

    def _add_user_to_group(self, group_name):
        group = Group.objects.get(name=group_name)
        user = self.user
        if not group in user.groups.all():
            user.groups.add(group)
            user.save()

    def _remove_user_from_group(self, group_name):
        group = Group.objects.get(name=group_name)
        user = self.user
        if group in user.groups.all():
            user.groups.remove(group)
            user.save()

    def my_projects(self):
        return self.organisation.all_projects()

    def my_unreported_projects(self):
        """
        Projects I may do SMS updates for that aren't linked through an SmsReporter yet, filtering out reporters that have no project set
        """
        return self.my_projects().exclude(pk__in=[r.project.pk for r in self.reporters.exclude(project=None)])

    def available_gateway_numbers(self):
        # TODO: user selectable gateways
        gw = Gateway.objects.get(name=self.GATEWAY_42IT)
        # find all "free" numbers
        numbers = GatewayNumber.objects.filter(gateway=gw).exclude(
            number__in=[r.gw_number.number for r in self.reporters.exclude(project=None)])
        return numbers

    def create_reporter(self, project=None):
        """
        Create a new SMSReporter object with a gateway number that is currently not in use
        """
        logger.debug("Entering: %s()" % who_am_i())
        try:
            #do we have a reporter without a project? Then we' use it to set the project
            reporter = self.reporters.get(project=None)
            if project:
                reporter.project = project
                reporter.save()
                self.enable_reporting(reporter)
                logger.info(u'%s(): SMS updating set up for project %s, user %s.' % (who_am_i(), project, self.user))
            logger.debug("Exiting: %s()" % who_am_i())
            return reporter
        except:
            numbers = self.available_gateway_numbers()
            if numbers:
                new_number = numbers[0]
                reporter = get_model('rsr', 'SmsReporter').objects.create(userprofile=self, project=project, gw_number=new_number)
                if project:
                    self.enable_reporting(reporter)
                    logger.info(
                        u'%s(): SMS updating set up for project %s, user %s.' % (who_am_i(), project, self.user))
                logger.debug("Exiting: %s()" % who_am_i())
                return reporter
            else:
                logger.error(u"%s(): No numbers defined for gateway. Can't create a reporter for user %s ." % (
                    who_am_i(), self.user))
                logger.debug("Exiting: %s()" % who_am_i())
                return None

    def find_reporter(self):
        """
        Find or create a reporter to validate phone number
        """
        logger.debug("Entering: %s()" % who_am_i())
        reporters = self.reporters.all()
        if reporters:
            logger.debug("Exiting: %s()" % who_am_i())
            return reporters[0]
        else:
            logger.debug("Exiting: %s()" % who_am_i())
            return self.create_reporter()

    def disable_reporting(self, reporter=None):
        """
        Disable SMS reporting for one or all projects linked to a userprofile
        """
        logger.debug("Entering: %s()" % who_am_i())
        if reporter and reporter.project:
            reporters = [reporter]
        else:
            reporters = self.reporters.exclude(project=None)  # exclude reporter that's not set up with a project
        for sms_reporter in reporters:
            try:
                sms_reporter.reporting_cancelled()
                logger.info(
                    u'SMS updating cancelled for project: %s Locals:\n %s\n\n' % (sms_reporter.project, locals(), ))
            except Exception, e:
                logger.exception('%s Locals:\n %s\n\n' % (e.message, locals(), ))
                #if self.validation == self.VALIDATED and self.reporters.count() < 1:
            #    try:
        #        user = self.user
        #        do_transition(self, self.TRANSITION_VALIDATE_PHONE_NUMBER, user)
        #    except Exception, e:
        #        logger.exception('%s Locals:\n %s\n\n' % (e.message, locals(), user))
        logger.debug("Exiting: %s()" % who_am_i())

    def disable_all_reporters(self):
        self.disable_reporting()

    def destroy_reporter(self, reporter=None):
        logger.debug("Entering: %s()" % who_am_i())
        if reporter:
            reporters = [reporter]
        else:
            reporters = self.reporters.all()
        for reporter in reporters:
            self.disable_reporting(reporter)
            reporter.delete()
        logger.debug("Exiting: %s()" % who_am_i())

    def disable_sms_update_workflow(self, admin_user=None):
        logger.debug("Entering: %s()" % who_am_i())
        # this profile's user
        user = self.user
        # user calling disable_sms_update_workflow
        admin_user = admin_user or user
        try:
            if (
                    self.state_equals(UserProfile.STATE_PHONE_DISABLED) or
                        Role.objects.get(name=self.ROLE_SMS_UPDATER) not in self.get_roles(user)
            ):
                logger.debug("Exiting: %s()" % who_am_i())
                return
            else:
                trans_ok = self.do_transition(self.TRANSITION_DISABLE_UPDATING, admin_user)
            if not trans_ok:
                logger.error('Error in UserProfileManager.disable_sms_update_workflow: Locals:\n %s\n\n' % (locals(),))
                logger.debug("Exiting: %s()" % who_am_i())
                return
            send_now([user], 'phone_disabled', extra_context={'phone_number': self.phone_number}, on_site=True)
            self.disable_all_reporters()
            logger.info('SMS updating disabled for user %s' % user.username)
        except Exception, e:
            logger.exception('%s Locals:\n %s\n\n' % (e.message, locals(), ))
        logger.debug("Exiting: %s()" % who_am_i())

    def confirm_validation(self, mo_sms):
        logger.debug("Entering: %s()" % who_am_i())
        try:
            logger.debug("Trying to find a reporter with number %s for user %s." % (mo_sms.receiver, self.user))
            reporter = self.reporters.get(gw_number=GatewayNumber.objects.get(number=mo_sms.receiver))
            if self.do_transition(self.TRANSITION_ENABLE_UPDATING, self.user):
                reporter.phone_confirmation()
                self.validation = self.VALIDATED
                self.save()
                logger.info(
                    "%s: transition to %s for user %s." % (who_am_i(), self.TRANSITION_ENABLE_UPDATING, self.user))
            else:
                logger.error(
                    'Error in UserProfile  Manager.process_sms: Not allowed to do transition %s for user %s. Locals:\n %s\n\n' % (
                        self.TRANSITION_VALIDATE_PHONE_NUMBER, self.user, locals()))
            self.enable_reporting()
        except Exception, e:
            logger.exception('Error in %s(): %s Locals:\n %s\n\n' % (who_am_i(), e.message, locals(), ))
        logger.debug("Exiting: %s()" % who_am_i())

    def enable_reporting(self, reporter=None):
        """
        Check for correct state and send email and SMS notifying the user about the enabled project
        If reporters=None we try to enable all reporters
        """
        logger.debug("Entering: %s()" % who_am_i())
        if reporter and reporter.project:
            reporters = [reporter]
        else:
            reporters = self.reporters.exclude(project=None)
            #if state_equals(self, [self.STATE_UPDATES_ENABLED, self.STATE_PHONE_NUMBER_VALIDATED]):
        if self.state_equals(self.STATE_UPDATES_ENABLED):
            for sms_reporter in reporters:
                #if state_equals(self, self.STATE_PHONE_NUMBER_VALIDATED):
                #    try:
                #        enabled = self.do_transition(self.TRANSITION_ENABLE_UPDATING, self.user)
                #    except Exception, e:
                #        logger.exception('%s Locals:\n %s\n\n' % (e.message, locals(),))
                try:
                    sms_reporter.reporting_enabled()
                    logger.info(
                        'Project enabled for updating: %s Locals:\n %s\n\n' % (sms_reporter.project.pk, locals(), ))
                except Exception, e:
                    logger.exception('%s Locals:\n %s\n\n' % (e.message, locals(), ))
        else:
            logger.error('UserProfile.enable_reporting() called with bad State: %s Locals:\n %s\n\n' % (
                self.get_state(), locals(), ))
        logger.debug("Exiting: %s()" % who_am_i())

    def enable_all_reporters(self):
        self.enable_reporting()

    def init_sms_update_workflow(self):
        '''
        Check that workflow exists ie the DB is setup correctly
        Disable reporters if we have any
        (Re)set state to STATE_PHONE_DISABLED
        '''
        logger.debug("Entering: %s()" % who_am_i())
        workflow = self.get_workflow()
        #in case of DB config bork:
        if not workflow:
            logger.error(
                'Error in %s. Workflow not defined for %s. Locals: %s' % (who_am_i(), self.user.username, locals()))
            return
            #set up current UserProfile with the workflow
        #this creates the WorkflowObjectRelation, sets initial State and
        #assigns permissions for the state (ObjectPermission)
        self.set_workflow(workflow)
        if state_equals(self, self.STATE_UPDATES_ENABLED):
            self.disable_all_reporters()
        self.set_initial_state()  # Phone disabled
        logger.debug("Exiting: %s()" % who_am_i())

    def add_phone_number(self, phone_number):
        """
        Set up workflow
        Transit to STATE_PHONE_NUMBER_ADDED
        Save phone number and generated validation code
        Get or create a Reporter
        Send a validation request
        """
        logger.debug("Entering: %s()" % who_am_i())
        user = self.user
        self.init_sms_update_workflow()
        #get workflow from model relation
        #check that we're allowed to do SMS updates
        if self.do_transition(self.TRANSITION_ADD_PHONE_NUMBER, user):
            self.validation = User.objects.make_random_password(length=6).upper()
            self.phone_number = phone_number
            self.save()
            # TODO: gateway selection!
            #gw_number = Gateway.objects.get(name=self.GATEWAY_42IT).gatewaynumber_set.all()[0]
            # Setup an initial SmsReporter for handling of registration SMSs so no project assigned to reporter yet.
            reporter = self.find_reporter()
            reporter.create_validation_request()
            logger.info('UserProfile.%s(): successfully set up workflow "%s" for user %s' % (
                who_am_i(), self.WORKFLOW_SMS_UPDATE, user.username, ))
        else:
            logger.info('UserProfile.%s(): user %s not allowed to set up workflow "%s"' % (
                who_am_i(), user.username, self.WORKFLOW_SMS_UPDATE, ))
        logger.debug("Exiting: %s()" % who_am_i())

    def has_permission(self, user, permission, roles=[]):
        """Grant SMS manager role if we're doing this for ourselves
        """
        #TODO: check that we have SMS updater role, if not we shouldn't get SMS manager role either :-p
        if self == user.get_profile() and Role.objects.get(name=self.ROLE_SMS_UPDATER) in self.get_roles(user):
            roles.append(Role.objects.get(name=self.ROLE_SMS_MANAGER))
        return super(UserProfile, self).has_permission(user, permission, roles)

    def has_perm_add_sms_updates(self):
        """used in myakvo navigation template to determin what links to show
        """
        return (
            self.has_permission(self.user, UserProfile.PERMISSION_ADD_SMS_UPDATES, []) or
            self.has_permission(self.user, UserProfile.PERMISSION_MANAGE_SMS_UPDATES, [])
        )

    has_perm_add_sms_updates.boolean = True  # make pretty icons in the admin list view
    has_perm_add_sms_updates.short_description = _('may create SMS project updates')
