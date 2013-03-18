# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

import mock
import pytest

from akvo.rsr.middleware import (get_domain,
                                 is_partner_site_instance,
                                 is_rsr_instance)


__all__ = ["test_get_domain",
           "test_is_partner_site_instance",
           "test_is_rsr_instance"]


@pytest.mark.parametrize(("input", "expected"), (
    ("localhost", "localhost"),
    ("www.akvo.org", "www.akvo.org"),
    ("akvo.akvoapp.org", "akvo.akvoapp.org"),
    ("subsubdomain.subdomain.domain.com", "subdomain.domain.com")
))
def test_get_domain(input, expected):
    request = mock.Mock()
    request.get_host = mock.Mock(method="get_host", return_value=input)
    assert get_domain(request) == expected


@pytest.mark.parametrize("host", (
    "akvo.org",
    "test.akvo.org",
    "www.akvo.org",
    "akvo.dev",
    "localhost"
))
def test_is_rsr_instance(host):
    assert is_rsr_instance(host)


@pytest.mark.parametrize("host", (
    "akvo.akvotest3.org",
    "cordaid.akvoapp.org",
    "simavi.akvotest.org"
))
def test_is_partner_site_instance(host):
    assert is_partner_site_instance(host)
