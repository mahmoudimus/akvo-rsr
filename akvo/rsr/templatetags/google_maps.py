# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from akvo.rsr.models import Organisation, Project

register = template.Library()


PROJECT_MARKER_ICON = getattr(settings, 'GOOGLE_MAPS_PROJECT_MARKER_ICON', '')
ORGANISATION_MARKER_ICON = getattr(settings, 'GOOGLE_MAPS_ORGANISATION_MARKER_ICON', '')


@register.inclusion_tag('inclusion_tags/google_map.html')
def google_map(object, width, height, zoom, marker_icon=None):
    is_project = isinstance(object, Project)
    is_organisation = isinstance(object, Organisation)
    if is_project:
        marker_icon = PROJECT_MARKER_ICON
    elif is_organisation:
        marker_icon = ORGANISATION_MARKER_ICON
    template_context = dict(object=object, width=width, height=height,
        zoom=zoom, marker_icon=marker_icon)
    return template_context


@register.inclusion_tag('inclusion_tags/google_global_project_map.html',
                        takes_context=True)
def google_global_project_map(context, map_type, width, height, zoom):
    data_url = reverse('global_project_map_json')
    marker_icon = PROJECT_MARKER_ICON
    template_context = dict(
        data_url=data_url,
        map_type=map_type,
        marker_icon=marker_icon,
        width=width,
        height=height,
        zoom=zoom,
        MEDIA_URL=settings.MEDIA_URL)
    return template_context


@register.inclusion_tag('inclusion_tags/google_global_organisation_map.html')
def google_global_organisation_map(map_type, width, height, zoom):
    data_url = reverse('global_organisation_map_json')
    marker_icon = ORGANISATION_MARKER_ICON
    template_context = dict(
        data_url=data_url,
        map_type=map_type,
        marker_icon=marker_icon,
        width=width,
        height=height,
        zoom=zoom,
        MEDIA_URL=settings.MEDIA_URL)
    return template_context


@register.inclusion_tag('inclusion_tags/google_global_project_map.html')
def google_organisation_projects_map(org_id, map_type, width, height, zoom):
    data_url = reverse('global_organisation_projects_map_json', args=[org_id])
    data_url = '%s?callback=?' % data_url
    marker_icon = PROJECT_MARKER_ICON
    template_context = dict(
        data_url=data_url,
        map_type=map_type,
        marker_icon=marker_icon,
        width=width,
        height=height,
        zoom=zoom,
        MEDIA_URL=settings.MEDIA_URL)
    return template_context


@register.inclusion_tag('inclusion_tags/google_global_project_map.html',
                        takes_context=True)
def google_queryset_projects_map(context, queryset, map_type, width, height, zoom):
    data_url = reverse('api_projects_cordinates')
    marker_icon = PROJECT_MARKER_ICON
    template_context = dict(
        data_url=data_url,
        map_type=map_type,
        marker_icon=marker_icon,
        projects=queryset,
        width=width,
        height=height,
        zoom=zoom,
        MEDIA_URL=settings.MEDIA_URL)
    return template_context
