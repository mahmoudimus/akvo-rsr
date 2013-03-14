# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from akvo.rsr.middleware import (get_domain, is_partner_site_instance,
                                 is_rsr_instance)


__all__ = ["test_get_domain",
           "test_is_partner_site_instance",
           "test_is_rsr_instance"]


class FakeRequest(object):
    
    def __init__(self, host="www.akvo.org"):
        self.host = host

    def get_host(self):
        return self.host

    
def test_get_domain():
    hosts = (("akvo.akvoapp.org", "akvo.akvoapp.org"),
             ("www.akvo.org", "www.akvo.org"),
             ("subsubdomain.subdomain.domain.com", "subdomain.domain.com"))
    for host, expected in hosts:
        assert get_domain(FakeRequest(host=host)) == expected


def pytest_generate_tests(metafunc):
    rsr_domains = ("akvo.org",
                   "test.akvo.org",
                   "www.akvo.org",
                   "akvo.dev",
                   "localhost")
    ps_domains = ("akvo.akvotest3.org",
                  "cordaid.akvoapp.org",
                  "simavi.akvotest.org")
    if "rsr_domain" in metafunc.funcargnames:
        metafunc.parametrize("rsr_domain", rsr_domains)
    elif "ps_domain" in metafunc.funcargnames:
        metafunc.parametrize("ps_domain", ps_domains)


def test_is_rsr_instance(rsr_domain):
    assert is_rsr_instance(rsr_domain)


def test_is_partner_site_instance(ps_domain):
    assert is_partner_site_instance(ps_domain)
