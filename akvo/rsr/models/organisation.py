# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from datetime import date, datetime, timedelta
from decimal import Decimal
from textwrap import dedent
from urlparse import urljoin

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.fields import ImageWithThumbnailsField

from akvo.rsr.iati_code_lists import IATI_LIST_ORGANISATION_TYPE
from akvo.rsr.utils import RSR_LIMITED_CHANGE, rsr_image_path

from location import OrganisationLocation
from model_utils import QuerySetManager
from partnership import Partnership


class Organisation(models.Model):
    """
    There are four types of organisations in RSR, called Field,
    Support, Funding and Sponsor partner respectively.
    """
    ORG_TYPE_NGO = 'N'
    ORG_TYPE_GOV = 'G'
    ORG_TYPE_COM = 'C'
    ORG_TYPE_KNO = 'K'
    ORG_TYPES = (
        (ORG_TYPE_NGO, _(u'NGO')),
        (ORG_TYPE_GOV, _(u'Governmental')),
        (ORG_TYPE_COM, _(u'Commercial')),
        (ORG_TYPE_KNO, _(u'Knowledge institution')),
    )

    def image_path(instance, file_name):
        return rsr_image_path(instance, file_name, 'db/org/%(instance_pk)s/%(file_name)s')

        #type = models.CharField(max_length=1, choices=PARNER_TYPES)

    #    field_partner = models.BooleanField(_(u'field partner'))
    #    support_partner = models.BooleanField(_(u'support partner'))
    #    funding_partner = models.BooleanField(_(u'funding partner'))
    #    sponsor_partner = models.BooleanField(_(u'sponsor partner'))

    name = models.CharField(_(u'name'), max_length=25, db_index=True, help_text=_(
        u'Short name which will appear in organisation and partner listings (25 characters).'))
    long_name = models.CharField(_(u'long name'), blank=True, max_length=75,
                                 help_text=_(u'Full name of organisation (75 characters).'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, default='en',
                                help_text=u'The main language of the organisation')
    organisation_type = models.CharField(_(u'organisation type'), max_length=1, db_index=True, choices=ORG_TYPES)
    new_organisation_type = models.IntegerField(_(u'IATI organisation type'), db_index=True,
                                                choices=IATI_LIST_ORGANISATION_TYPE, default=22,
                                                help_text=u'Check that this field is set to an organisation type that matches your organisation.')
    iati_org_id = models.CharField(_(u'IATI organisation ID'), max_length=75, blank=True, null=True, db_index=True)

    logo = ImageWithThumbnailsField(
        _(u'logo'), blank=True, upload_to=image_path, thumbnail={'size': (360, 270)},
        extra_thumbnails={'map_thumb': {'size': (160, 120), 'options': ('autocrop',)}},
        help_text=_(u'Logos should be approximately 360x270 pixels (approx. 100-200kB in size) on a white background.'),
    )

    url = models.URLField(blank=True, verify_exists=False,
                          help_text=_(u'Enter the full address of your web site, beginning with http://.'))

    phone = models.CharField(_(u'phone'), blank=True, max_length=20, help_text=_(u'(20 characters).'))
    mobile = models.CharField(_(u'mobile'), blank=True, max_length=20, help_text=_(u'(20 characters).'))
    fax = models.CharField(_(u'fax'), blank=True, max_length=20, help_text=_(u'(20 characters).'))
    contact_person = models.CharField(_(u'contact person'), blank=True, max_length=30, help_text=_(
        u'Name of external contact person for your organisation (30 characters).'))
    contact_email = models.CharField(_(u'contact email'), blank=True, max_length=50, help_text=_(
        u'Email to which inquiries about your organisation should be sent (50 characters).'))
    description = models.TextField(_(u'description'), blank=True, help_text=_(u'Describe your organisation.'))

    # old_locations = generic.GenericRelation(Location)
    primary_location = models.ForeignKey(OrganisationLocation, null=True, on_delete=models.SET_NULL)

    # Managers, one default, one custom
    # objects = models.Manager()
    objects = QuerySetManager()
    # projects = ProjectsQuerySetManager()

    @models.permalink
    def get_absolute_url(self):
        return ('organisation_main', (), {'org_id': self.pk})

    # @property
    # def primary_location(self):
    #     '''Returns an organisations's primary location'''
    #     qs = self.locations.filter(primary=True)
    #     qs = qs.exclude(latitude=0, longitude=0)
    #     if qs:
    #         location = qs[0]
    #         return location
    #     return

    class QuerySet(QuerySet):
        def has_location(self):
            return self.filter(primary_location__isnull=False)

        def partners(self, partner_type):
            "return the organisations in the queryset that are partners of type partner_type"
            return self.filter(partnerships__partner_type__exact=partner_type).distinct()

        def allpartners(self):
            return self.distinct()

        def fieldpartners(self):
            return self.partners(Partnership.FIELD_PARTNER)

        def fundingpartners(self):
            return self.partners(Partnership.FUNDING_PARTNER)

        def sponsorpartners(self):
            return self.partners(Partnership.SPONSOR_PARTNER)

        def supportpartners(self):
            return self.partners(Partnership.SUPPORT_PARTNER)

        def ngos(self):
            return self.filter(organisation_type__exact=Organisation.ORG_TYPE_NGO)

        def governmental(self):
            return self.filter(organisation_type__exact=Organisation.ORG_TYPE_GOV)

        def commercial(self):
            return self.filter(organisation_type__exact=Organisation.ORG_TYPE_COM)

        def knowledge(self):
            return self.filter(organisation_type__exact=Organisation.ORG_TYPE_KNO)

    def __unicode__(self):
        return self.name

    def is_partner_type(self, partner_type):
        "returns True if the organisation is a partner of type partner_type to at least one project"
        return self.partnerships.filter(partner_type__exact=partner_type).count() > 0

    def is_field_partner(self):
        "returns True if the organisation is a field partner to at least one project"
        return self.is_partner_type(Partnership.FIELD_PARTNER)

    def is_funding_partner(self):
        "returns True if the organisation is a funding partner to at least one project"
        return self.is_partner_type(Partnership.FUNDING_PARTNER)

    def is_sponsor_partner(self):
        "returns True if the organisation is a sponsor partner to at least one project"
        return self.is_partner_type(Partnership.SPONSOR_PARTNER)

    def is_support_partner(self):
        "returns True if the organisation is a support partner to at least one project"
        return self.is_partner_type(Partnership.SUPPORT_PARTNER)

    def website(self):
        return '<a href="%s">%s</a>' % (self.url, self.url,)

    website.allow_tags = True

    def published_projects(self):
        "returns a queryset with published projects that has self as any kind of partner"
        return self.projects.published().distinct()

    def all_projects(self):
        "returns a queryset with all projects that has self as any kind of partner"
        return self.projects.all().distinct()

    def active_projects(self):
        return self.published_projects().status_not_cancelled().status_not_archived()

    def partners(self):
        "returns a queryset of all organisations that self has at least one project in common with, excluding self"
        return self.published_projects().all_partners().exclude(id__exact=self.id)

    # New API

    def euros_pledged(self):
        "How much € the organisation has pledged to projects it is a partner to"
        return self.active_projects().euros().filter(
            partnerships__organisation__exact=self, partnerships__partner_type__exact=Partnership.FUNDING_PARTNER
        ).aggregate(
            euros_pledged=Sum('partnerships__funding_amount')
        )['euros_pledged'] or 0

    def dollars_pledged(self):
        "How much $ the organisation has pledged to projects"
        return self.active_projects().dollars().filter(
            partnerships__organisation__exact=self, partnerships__partner_type__exact=Partnership.FUNDING_PARTNER
        ).aggregate(
            dollars_pledged=Sum('partnerships__funding_amount')
        )['dollars_pledged'] or 0

    def euro_projects_count(self):
        "How many projects with budget in € the organisation is a partner to"
        return self.published_projects().euros().distinct().count()

    def dollar_projects_count(self):
        "How many projects with budget in $ the organisation is a partner to"
        return self.published_projects().dollars().distinct().count()

    def _aggregate_funds_needed(self, projects):
        return sum(projects.values_list('funds_needed', flat=True))

    def euro_funds_needed(self):
        "How much is still needed to fully fund all projects with € budget that the organiastion is a partner to"
        # the ORM aggregate() doesn't work here since we may have multiple partnership relations to the same project
        return self._aggregate_funds_needed(self.published_projects().euros().distinct())

    def dollar_funds_needed(self):
        "How much is still needed to fully fund all projects with $ budget that the organiastion is a partner to"
        # the ORM aggregate() doesn't work here since we may have multiple partnership relations to the same project
        return self._aggregate_funds_needed(self.published_projects().dollars().distinct())

    # New API end

    class Meta:
        verbose_name = _(u'organisation')
        verbose_name_plural = _(u'organisations')
        ordering = ['name']
        permissions = (
            ("%s_organisation" % RSR_LIMITED_CHANGE, u'RSR limited change organisation'),
        )

