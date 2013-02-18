# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module. 
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.
from copy import deepcopy
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse

from tastypie import fields
from tastypie import http

from tastypie.authentication import ApiKeyAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from tastypie.utils.mime import build_content_type

from cacheback.base import Job

from akvo.api.fields import ConditionalFullToManyField, ConditionalFullToOneField, bundle_related_data_info_factory
from akvo.rsr.models import (
    Benchmark, Benchmarkname, BudgetItem, BudgetItemLabel, Category, Country, FocusArea, Goal, Link,
    Organisation, OrganisationLocation, Partnership, Project, ProjectLocation, ProjectUpdate,
    ProjectComment, UserProfile, Invoice
)

from akvo.rsr.utils import PAYPAL_INVOICE_STATUS_COMPLETE

__all__ = [
    'BenchmarkResource',
    'BenchmarknameResource',
    'BudgetItemResource',
    'BudgetItemLabelResource',
    'CategoryResource',
    'CountryResource',
    'FocusAreaResource',
    'GoalResource',
    'InvoiceResource',
    'LinkResource',
    'OrganisationResource',
    'OrganisationLocationResource',
    'OrganisationMapResource',
    'PartnershipResource',
    'ProjectResource',
    'ProjectCommentResource',
    'ProjectLocationResource',
    'ProjectMapResource',
    'ProjectUpdateResource',
    'UserResource',
    'UserProfileResource',
]

def get_extra_thumbnails(image_field):
    try:
        thumbs = image_field.extra_thumbnails
        return dict([(key, thumbs[key].absolute_url) for key in thumbs.keys()])
    except:
        return None


class CachedResourceJob(Job):

    def __init__(self, resource, request, kwargs):
        self.resource = resource
        self.request = request
        self.kwargs = kwargs
        super(CachedResourceJob, self).__init__()

    def fetch(self, url):
        """
        emulates most of Resource.get_list() but stops before calling create_response()
        """
        resource = self.resource
        request = self.request
        kwargs = self.kwargs
        # code of Resource.get_list()
        objects = resource.obj_get_list(request=request, **resource.remove_api_resource_names(kwargs))
        sorted_objects = resource.apply_sorting(objects, options=request.GET)

        paginator = resource._meta.paginator_class(request.GET, sorted_objects, resource_uri=resource.get_resource_uri(), limit=resource._meta.limit)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [resource.build_bundle(obj=obj, request=request) for obj in to_be_serialized['objects']]
        # add metadata to bundle to keep track of "depth", "ancestor" and "full" info
        for bundle in bundles:
            bundle.related_info = bundle_related_data_info_factory(request=request)
            # end add
        to_be_serialized['objects'] = [resource.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = resource.alter_list_data_to_serialize(request, to_be_serialized)
        # code of Resource.create_response() but only as far as serializing
        # meaning the serialized result is what gets cached
        desired_format = resource.determine_format(request)
        return resource.serialize(request, to_be_serialized, desired_format).encode("utf8").encode("zlib")


class ConditionalFullResource(ModelResource):

    def apply_filters(self, request, applicable_filters):
        """
        An ORM-specific implementation of ``apply_filters``.

        The default simply applies the ``applicable_filters`` as ``**kwargs``,
        but should make it possible to do more advanced things.

        Here we override to check for a 'distinct' query string variable,
        if it's equal to True we apply distinct() to the queryset after filtering.
        """
        distinct = request.GET.get('distinct', False) == 'True'
        if distinct:
            return self.get_object_list(request).filter(**applicable_filters).distinct()
        else:
            return self.get_object_list(request).filter(**applicable_filters)

    def get_list(self, request, **kwargs):
        """
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        --------------------------------------
        This is a "gutted" get_list where most of the code has been moved to CachedResourceJob.fetch so that cacheback can
        do its thing and only run the original get_list if we don't have anything in the cache
        """
        desired_format = self.determine_format(request)
        cached_resource = CachedResourceJob(self, request, kwargs)
        url = "%s?%s" % (request.path, request.META['QUERY_STRING'])
        serialized = cached_resource.get(url).decode("zlib").decode("utf8")
        return HttpResponse(content=serialized, content_type=build_content_type(desired_format))

    def get_detail(self, request, **kwargs):
        """
        Returns a single serialized resource.

        Calls ``cached_obj_get/obj_get`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        try:
            obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        bundle = self.build_bundle(obj=obj, request=request)
        # add metadata to bundle to keep track of "depth", "ancestor" and "full" info
        bundle.related_info = bundle_related_data_info_factory(request=request)
        # end add
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)


class BenchmarkResource(ConditionalFullResource):
    project     = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')
    category    = ConditionalFullToOneField('akvo.api.resources.CategoryResource', 'category')
    name        = ConditionalFullToOneField('akvo.api.resources.BenchmarknameResource', 'name', full=True)

    class Meta:
        allowed_methods = ['get']
        queryset        = Benchmark.objects.all()
        resource_name   = 'benchmark'
        filtering       = dict(
            # foreign keys
            category    = ALL_WITH_RELATIONS,
            name        = ALL_WITH_RELATIONS,
            project     = ALL_WITH_RELATIONS,
        )


class BenchmarknameResource(ConditionalFullResource):
    class Meta:
        allowed_methods = ['get']
        queryset        = Benchmarkname.objects.all()
        resource_name   = 'benchmarkname'
        filtering       = dict(
            # other fields
            name        = ALL,
        )


class BudgetItemResource(ConditionalFullResource):
    label   = ConditionalFullToOneField('akvo.api.resources.BudgetItemLabelResource', 'label', full=True)
    project = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')

    class Meta:
        allowed_methods = ['get']
        queryset        = BudgetItem.objects.all()
        resource_name   = 'budget_item'
        filtering       = dict(
            # foreign keys
            label       = ALL_WITH_RELATIONS,
            project     = ALL_WITH_RELATIONS,
        )


class BudgetItemLabelResource(ConditionalFullResource):
    class Meta:
        allowed_methods = ['get']
        queryset        = BudgetItemLabel.objects.all()
        resource_name   = 'budget_item_label'
        filtering       = dict(
            # other fields
            label       = ALL,
        )


class CategoryResource(ConditionalFullResource):
    class Meta:
        allowed_methods = ['get']
        queryset        = Category.objects.all()
        resource_name   = 'category'
        filtering       = dict(
            # other fields
            name        = ALL,
            # foreign keys
            focus_area  = ALL_WITH_RELATIONS,
        )


class CountryResource(ConditionalFullResource):
    class Meta:
        allowed_methods = ['get']
        queryset        = Country.objects.all()
        resource_name   = 'country'
        filtering       = dict(
            # other fields
            iso_code        = ALL,
            continent_code  = ALL,
        )


class FocusAreaResource(ConditionalFullResource):
    categories      = ConditionalFullToManyField('akvo.api.resources.CategoryResource', 'categories')

    class Meta:
        allowed_methods = ['get']
        queryset        = FocusArea.objects.all()
        resource_name   = 'focus_area'
        filtering       = dict(
            # other fields
            slug        = ALL,
        )


class GoalResource(ConditionalFullResource):
    project = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')

    class Meta:
        allowed_methods = ['get']
        queryset        = Goal.objects.all()
        resource_name   = 'goal'
        filtering       = dict(
            # foreign keys
            project     = ALL_WITH_RELATIONS,
        )


class InvoiceResource(ConditionalFullResource):
    project = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')

    class Meta:
        allowed_methods = ['get']
        queryset        = Invoice.objects.filter(status__exact=PAYPAL_INVOICE_STATUS_COMPLETE)
        resource_name   = 'invoice'
        fields          = ['amount', 'amount_received', 'is_anonymous',]
        filtering       = dict(
            # foreign keys
            project     = ALL_WITH_RELATIONS,
            user        = ALL_WITH_RELATIONS,
        )

    def dehydrate(self, bundle):
        """ Add name and email for non-anonymous donators
        """
        bundle = super(InvoiceResource, self).dehydrate(bundle)
        if not bundle.obj.is_anonymous:
            bundle.data['email'] = bundle.obj.email
            bundle.data['name'] = bundle.obj.name
        return bundle


class LinkResource(ConditionalFullResource):
    project = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')

    class Meta:
        allowed_methods = ['get']
        queryset        = Link.objects.all()
        resource_name   = 'link'
        filtering       = dict(
            # foreign keys
            project     = ALL_WITH_RELATIONS,
        )


class OrganisationResource(ConditionalFullResource):
    partnerships        = ConditionalFullToManyField(
        'akvo.api.resources.PartnershipResource',
        'partnerships',
        help_text='Show the projects the organisation is related to and how.'
    )
    locations           = ConditionalFullToManyField('akvo.api.resources.OrganisationLocationResource', 'locations', null=True)
    primary_location    = fields.ToOneField('akvo.api.resources.OrganisationLocationResource', 'primary_location', full=True, null=True)

    class Meta:
        allowed_methods         = ['get']
        queryset                = Organisation.objects.all()
        resource_name           = 'organisation'
        include_absolute_url    = True

        filtering       = dict(
            # other fields
            iati_org_id         = ALL,
            name                = ALL,
            organisation_type   = ALL,
            # foreign keys
            locations           = ALL_WITH_RELATIONS,
            partnerships        = ALL_WITH_RELATIONS,
        )

    def dehydrate(self, bundle):
        """ add thumbnails inline info for Organisation.logo
        """
        bundle = super(OrganisationResource, self).dehydrate(bundle)
        bundle.data['logo'] = {
            'original': bundle.data['logo'],
            'thumbnails': get_extra_thumbnails(bundle.obj.logo),
        }
        return bundle


class OrganisationLocationResource(ConditionalFullResource):
    organisation    = ConditionalFullToOneField(OrganisationResource, 'location_target')
    country         = ConditionalFullToOneField(CountryResource, 'country')

    class Meta:
        allowed_methods = ['get']
        queryset        = OrganisationLocation.objects.all()
        resource_name   = 'organisation_location'
        filtering       = dict(
            # foreign keys
            organisation= ALL_WITH_RELATIONS,
            country     = ALL_WITH_RELATIONS,
        )


class OrganisationMapResource(ConditionalFullResource):
    """
    a limited resource for delivering data to be used when creating maps
    """
    locations           = ConditionalFullToManyField('akvo.api.resources.OrganisationLocationResource', 'locations', null=True)
    primary_location    = fields.ToOneField('akvo.api.resources.OrganisationLocationResource', 'primary_location', full=True, null=True)

    class Meta:
        allowed_methods         = ['get']
        queryset                = Organisation.objects.all()
        resource_name           = 'map_for_organisation'
        include_absolute_url    = True

        filtering       = dict(
            # other fields
            iati_org_id         = ALL,
            name                = ALL,
            organisation_type   = ALL,
            # foreign keys
            locations           = ALL_WITH_RELATIONS,
            partnerships        = ALL_WITH_RELATIONS,
            )

    def dehydrate(self, bundle):
        """ add thumbnails inline info for Organisation.logo
        """
        bundle = super(OrganisationMapResource, self).dehydrate(bundle)
        del bundle.data['description']
        bundle.data['logo'] = {
            'original': bundle.data['logo'],
            'thumbnails': get_extra_thumbnails(bundle.obj.logo),
            }
        return bundle


class PartnershipResource(ConditionalFullResource):
    organisation    = ConditionalFullToOneField('akvo.api.resources.OrganisationResource', 'organisation')
    project         = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')

    def __init__(self, api_name=None):
        """ override to be able to create custom help_text on the partner_type field
        """
        super(PartnershipResource, self).__init__(api_name=None)
        self.fields['partner_type'].help_text = "Uses the following key-value pair list: {%s}" % ', '.join(
            ['"%s": "%s"' % (k, v) for k, v in Partnership.PARTNER_TYPES]
        )

    class Meta:
        allowed_methods = ['get']
        queryset        = Partnership.objects.all()
        resource_name   = 'partnership'
        filtering       = dict(organisation=ALL_WITH_RELATIONS)
        filtering       = dict(
            # other fields
            iati_activity_id    = ALL,
            internal_id         = ALL,
            partner_type        = ALL,
            # foreign keys
            organisation        = ALL_WITH_RELATIONS,
            project             = ALL_WITH_RELATIONS,
        )


class ProjectResource(ConditionalFullResource):
    benchmarks          = ConditionalFullToManyField('akvo.api.resources.BenchmarkResource', 'benchmarks',)
    budget_items        = ConditionalFullToManyField('akvo.api.resources.BudgetItemResource', 'budget_items')
    categories          = ConditionalFullToManyField('akvo.api.resources.CategoryResource', 'categories')
    goals               = ConditionalFullToManyField('akvo.api.resources.GoalResource', 'goals')
    invoices            = ConditionalFullToManyField('akvo.api.resources.InvoiceResource', 'invoices')
    links               = ConditionalFullToManyField('akvo.api.resources.LinkResource', 'links')
    locations           = ConditionalFullToManyField('akvo.api.resources.ProjectLocationResource', 'locations')
    partnerships        = ConditionalFullToManyField('akvo.api.resources.PartnershipResource', 'partnerships',)
    primary_location    = fields.ToOneField('akvo.api.resources.ProjectLocationResource', 'primary_location', full=True, null=True)
    project_comments    = ConditionalFullToManyField('akvo.api.resources.ProjectCommentResource', 'comments')
    project_updates     = ConditionalFullToManyField('akvo.api.resources.ProjectUpdateResource', 'project_updates')

    class Meta:
        allowed_methods         = ['get']
        queryset                = Project.objects.published()
        resource_name           = 'project'
        include_absolute_url    = True

        filtering               = dict(
            # other fields
            status              = ALL,
            title               = ALL,
            budget              = ALL,
            funds               = ALL,
            funds_needed        = ALL,
            # foreign keys
            benchmarks          = ALL_WITH_RELATIONS,
            budget_items        = ALL_WITH_RELATIONS,
            categories          = ALL_WITH_RELATIONS,
            goals               = ALL_WITH_RELATIONS,
            invoices            = ALL_WITH_RELATIONS,
            links               = ALL_WITH_RELATIONS,
            locations           = ALL_WITH_RELATIONS,
            partnerships        = ALL_WITH_RELATIONS,
            project_comments    = ALL_WITH_RELATIONS,
            project_updates     = ALL_WITH_RELATIONS,
        )

    def dehydrate(self, bundle):
        """ add thumbnails inline info for Project.current_image
        """
        bundle = super(ProjectResource, self).dehydrate(bundle)
        bundle.data['current_image'] = {
            'original': bundle.data['current_image'],
            'thumbnails': get_extra_thumbnails(bundle.obj.current_image),
        }
        return bundle


class ProjectCommentResource(ConditionalFullResource):
    project = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')

    class Meta:
        allowed_methods = ['get']
        queryset        = ProjectComment.objects.all()
        resource_name   = 'project_comment'
        filtering       = dict(
            # other fields
            time        = ALL,
            # foreign keys
            project     = ALL_WITH_RELATIONS,
            user        = ALL_WITH_RELATIONS,
        )


class ProjectLocationResource(ConditionalFullResource):
    project = ConditionalFullToOneField(ProjectResource, 'location_target')
    country = ConditionalFullToOneField(CountryResource, 'country')

    class Meta:
        allowed_methods = ['get']
        queryset        = ProjectLocation.objects.all()
        resource_name   = 'project_location'
        filtering       = dict(
            # other fields
            latitude    = ALL,
            longitude   = ALL,
            primary     = ALL,
            # foreign keys
            country     = ALL_WITH_RELATIONS,
            project     = ALL_WITH_RELATIONS,
        )


class ProjectMapResource(ConditionalFullResource):
    """
    a limited resource for delivering data to be used when creating maps
    """
    locations           = ConditionalFullToManyField('akvo.api.resources.ProjectLocationResource', 'locations')
    primary_location    = fields.ToOneField('akvo.api.resources.ProjectLocationResource', 'primary_location', full=True, null=True)

    class Meta:
        allowed_methods         = ['get']
        queryset                = Project.objects.published()
        resource_name           = 'map_for_project'
        include_absolute_url    = True

        filtering               = dict(
            # other fields
            status              = ALL,
            title               = ALL,
            budget              = ALL,
            funds               = ALL,
            funds_needed        = ALL,
            # foreign keys
            benchmarks          = ALL_WITH_RELATIONS,
            budget_items        = ALL_WITH_RELATIONS,
            categories          = ALL_WITH_RELATIONS,
            goals               = ALL_WITH_RELATIONS,
            invoices            = ALL_WITH_RELATIONS,
            links               = ALL_WITH_RELATIONS,
            locations           = ALL_WITH_RELATIONS,
            partnerships        = ALL_WITH_RELATIONS,
            project_comments    = ALL_WITH_RELATIONS,
            project_updates     = ALL_WITH_RELATIONS,
            )

    def dehydrate(self, bundle):
        """ add thumbnails inline info for Project.current_image
        """
        bundle = super(ProjectMapResource, self).dehydrate(bundle)
        ignored_fields = ('goals_overview', 'current_status', 'project_plan', 'sustainability', 'background', 'project_rating', 'notes',)
        for field in ignored_fields:
            del bundle.data[field]
        bundle.data['current_image'] = {
            'original': bundle.data['current_image'],
            'thumbnails': get_extra_thumbnails(bundle.obj.current_image),
            }
        return bundle


class ProjectUpdateResource(ConditionalFullResource):
    project = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')
    user    = ConditionalFullToOneField('akvo.api.resources.UserResource', 'user')

    class Meta:
        allowed_methods         = ['get']
        queryset                = ProjectUpdate.objects.all()
        resource_name           = 'project_update'
        include_absolute_url    = True

        filtering               = dict(
            # other fields
            time                = ALL,
            time_last_updated   = ALL,
            title               = ALL,
            update_method       = ALL,
            # foreign keys
            project             = ALL_WITH_RELATIONS,
            user                = ALL_WITH_RELATIONS,
        )


class UserProfileResource(ConditionalFullResource):
    organisation    = ConditionalFullToOneField('akvo.api.resources.OrganisationResource', 'organisation')
    user            = ConditionalFullToOneField('akvo.api.resources.UserResource', 'user')

    class Meta:
        authentication  = ApiKeyAuthentication()
        allowed_methods = ['get']
        queryset        = UserProfile.objects.filter(user__is_active=True)
        resource_name   = 'user_profile'
        fields          = ['organisation', 'user',]
        filtering       = dict(
            # foreign keys
            user            = ALL_WITH_RELATIONS,
            organisation    = ALL_WITH_RELATIONS,
        )

    def get_object_list(self, request):
        """ Limit access to the users in your own organisation
        """
        organisation = request.user.get_profile().organisation
        return UserProfile.objects.filter(organisation=organisation)

    def dehydrate(self, bundle):
        """ Add meta fields showing if the user profile is an organisation admin or an organisation editor
        """
        bundle = super(UserProfileResource, self).dehydrate(bundle)
        bundle.data['is_org_admin'] = bundle.obj.get_is_org_admin()
        bundle.data['is_org_editor'] = bundle.obj.get_is_org_editor()
        return bundle


class UserResource(ConditionalFullResource):
    user_profile = ConditionalFullToOneField('akvo.api.resources.UserProfileResource', 'userprofile', null=True)

    class Meta:
        authentication  = ApiKeyAuthentication()
        allowed_methods = ['get']
        queryset = User.objects.filter(is_active=True)
        resource_name = 'user'
        fields = ['first_name', 'last_name', 'last_login', ]
        filtering       = dict(
            # foreign keys
            userprofile  = ALL_WITH_RELATIONS,
        )

    def dehydrate(self, bundle):
        """ Workaround for the overloading of 'username' when used in the query.
            It is needed for the authentication, but the filtering machinery
            intercepts and complains that the 'username' field doesn't allow filtering.
            So instead of having username in the fields list we add it here

            The adding is conditional, only add fields for users in the same organisation
            as request.user which is the API key owner

            For other users delete the user_profile field
        """
        bundle = super(UserResource, self).dehydrate(bundle)
        if self._meta.authentication.is_authenticated(bundle.request):
            if getattr(bundle.request.user, 'get_profile', False):
                # get the org of the API key owner
                organisation = bundle.request.user.get_profile().organisation
            else:
                organisation = None
            # find out if the user has a profile that's associated with the API key owner org
            profile = UserProfile.objects.filter(organisation=organisation, user__id=bundle.obj.id)
        if profile:
            bundle.data['username'] = bundle.obj.username
            bundle.data['email'] = bundle.obj.email
        else:
            del bundle.data['user_profile']
        return bundle

