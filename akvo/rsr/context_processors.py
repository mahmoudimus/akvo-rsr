# -*- coding: utf-8 -*-
"""
    Akvo RSR is covered by the GNU Affero General Public License.
    See more details in the license.txt file located at the root folder of the
    Akvo RSR module. For additional details on the GNU license please
    see < http://www.gnu.org/licenses/agpl.html >.
"""
from __future__ import absolute_import
import django
from django.contrib.sites.models import Site


def extra_context(request):
    current_site = Site.objects.get_current()
    django_version = django.get_version()
    template_context = dict(current_site=current_site,
        django_version=django_version)
    return template_context


def site_section_massage(request):
    """Adds 'site_section' context variable to pages that are rendered from non
    RSR views. This to be able to set the correct toolbar item."""
    request_url = request.get_full_path().split('?')[0]
    if not request_url.startswith('/rsr/notices') \
        and not request_url.startswith('/rsr/accounts'):
        return dict()

    template_context = dict(site_section='myakvo')
    return template_context
