# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from datetime import date, datetime, timedelta
from decimal import Decimal
from textwrap import dedent
from urlparse import urljoin

import logging

logger = logging.getLogger('akvo.rsr')

from django.db import models
from django.db.models import get_model
from django.contrib.sites.models import Site

from akvo.rsr.utils import RSR_LIMITED_CHANGE, who_am_i, send_now

class SmsReporterManager(models.Manager):
    def select(self, profile=None, gw_number=None, project=None):
        #need either gw_number or project
        if gw_number or project:
            if gw_number:
                return self.get(userprofile=profile, gw_number=gw_number)
            else:
                return self.get(userprofile=profile, project=project)
        raise SmsReporter.DoesNotExist


class SmsReporter(models.Model):
    """
    Mapping between projects, gateway phone numbers and users phones
    """
    userprofile = models.ForeignKey('UserProfile', related_name='reporters')
    gw_number = models.ForeignKey('GatewayNumber')
    project = models.ForeignKey('Project', null=True, blank=True, )

    objects = SmsReporterManager()

    class Meta:
        unique_together = ('userprofile', 'gw_number', 'project',)
        permissions = (
            ("%s_smsreporter" % RSR_LIMITED_CHANGE, u'RSR limited change sms reporter'),
        )

    def __unicode__(self):
        if self.project:
            return "%s:%s:%s" % (self.userprofile.user.username, self.gw_number, self.project)
        else:
            return "%s:%s" % (self.userprofile.user.username, self.gw_number)

    def create_sms_update(self, mo_sms):
        """
        Create a project update from an incoming SMS
        """
        logger.debug("Entering: %s()" % who_am_i())
        if not self.project:
            logger.error("No project defined for SmsReporter %s. Locals:\n %s\n\n" % (self.__unicode__, locals()))
            return False
        update_data = {
            'project': self.project,
            'user': self.userprofile.user,
            'title': 'SMS update',
            'update_method': 'S',
            'text': mo_sms.message,
            'time': mo_sms.saved_at,
        }
        try:
            update = get_model('rsr', 'ProjectUpdate').objects.create(**update_data)
            logger.info("Created new project update from sms. ProjectUpdate.id: %d" % update.pk)
            self.update_received(update)
            logger.debug("Exiting: %s()" % who_am_i())
            return update
        except Exception, e:
            logger.exception(
                "Exception when creating an sms project update. Error: %s Locals:\n %s\n\n" % (e.message, locals(), ))
            logger.debug("Exiting: %s()" % who_am_i())
            return False

    def update_received(self, update):
        profile = self.userprofile
        extra_context = {
            'gw_number': self.gw_number,
            'phone_number': profile.phone_number,
            'project': self.project,
            'update': update,
            'domain': Site.objects.get_current().domain,
        }
        send_now([profile.user], 'update_received', extra_context=extra_context, on_site=True)

    def reporting_cancelled(self, set_delete=False):
        profile = self.userprofile
        #self.delete = set_delete
        extra_context = {
            'gw_number': self.gw_number,
            'phone_number': profile.phone_number,
            'project': self.project,
        }
        send_now([profile.user], 'reporting_cancelled', extra_context=extra_context, on_site=True)

    def reporting_enabled(self):
        profile = self.userprofile
        extra_context = {
            'gw_number': self.gw_number,
            'phone_number': profile.phone_number,
            'project': self.project,
        }
        send_now([profile.user], 'reporting_enabled', extra_context=extra_context, on_site=True)

    def create_validation_request(self):
        """
        send validation code through email and an SMS that the user can easily
        reply to with the code to validate the phone number
        """
        # check we aren't already validated
        profile = self.userprofile
        if profile.validation != profile.VALIDATED:
            extra_context = {
                'gw_number': self.gw_number,
                'validation': profile.validation,
                'phone_number': profile.phone_number,
            }
            send_now([profile.user], 'phone_added', extra_context=extra_context, on_site=True)

    def phone_confirmation(self):
        profile = self.userprofile
        extra_context = {
            'gw_number': self.gw_number,
            'phone_number': profile.phone_number,
            'domain': Site.objects.get_current().domain,
        }
        send_now([profile.user], 'phone_confirmed', extra_context=extra_context, on_site=True)
