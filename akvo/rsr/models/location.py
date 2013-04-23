# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from country import Country
# from organisation import Organisation
# from project import Project

from akvo.rsr.fields import LatitudeField, LongitudeField


class BaseLocation(models.Model):
    _help_text = _(u"Go to <a href='http://itouchmap.com/latlong.html' target='_blank'>iTouchMap.com</a> "
                   u'to get the decimal coordinates of your project.')
    latitude = LatitudeField(_(u'latitude'), db_index=True, default=0, help_text=_help_text)
    longitude = LongitudeField(_(u'longitude'), db_index=True, default=0, help_text=_help_text)
    city = models.CharField(_(u'city'), blank=True, max_length=255, help_text=_('(255 characters).'))
    state = models.CharField(_(u'state'), blank=True, max_length=255, help_text=_('(255 characters).'))
    country = models.ForeignKey(Country, verbose_name=_(u'country'))
    address_1 = models.CharField(_(u'address 1'), max_length=255, blank=True, help_text=_('(255 characters).'))
    address_2 = models.CharField(_(u'address 2'), max_length=255, blank=True, help_text=_('(255 characters).'))
    postcode = models.CharField(_(u'postcode'), max_length=10, blank=True, help_text=_('(10 characters).'))
    primary = models.BooleanField(_(u'primary location'), db_index=True, default=True)

    def __unicode__(self):
        return u'%s, %s (%s)' % (self.city, self.state, self.country)

    def save(self, *args, **kwargs):
        super(BaseLocation, self).save(*args, **kwargs)
        if self.primary:
            location_target = self.location_target
            # this is probably redundant since the admin form saving should handle this
            # but if we ever save a location from other code it's an extra safety
            location_target.locations.exclude(pk__exact=self.pk).update(primary=False)
            location_target.primary_location = self
            location_target.save()

    class Meta:
        abstract = True
        ordering = ['-primary', ]


class OrganisationLocation(BaseLocation):
    # the organisation that's related to this location
    location_target = models.ForeignKey('Organisation', null=True, related_name='locations')


class ProjectLocation(BaseLocation):
    # the project that's related to this location
    location_target = models.ForeignKey('Project', null=True, related_name='locations')

