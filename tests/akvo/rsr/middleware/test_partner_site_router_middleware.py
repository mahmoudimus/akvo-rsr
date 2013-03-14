# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from akvo.rsr.middleware import (get_domain,
                                 is_partner_site_instance,
                                 is_rsr_instance)


__all__ = ["test_get_domain",
           "test_is_partner_site_instance",
           "test_is_rsr_instance"]


class FakeRequest(object):
    
    def __init__(self, host="www.akvo.org"):
        self.host = host

    def get_host(self):
        return self.host

    


def pytest_generate_tests(metafunc):
    hosts = (("localhost", "localhost"),
             ("akvo.akvoapp.org", "akvo.akvoapp.org"),
             ("www.akvo.org", "www.akvo.org"),
             ("subsubdomain.subdomain.domain.com", "subdomain.domain.com"))
    rsr_domains = ("akvo.org",
                   "test.akvo.org",
                   "www.akvo.org",
                   "akvo.dev",
                   "localhost")
    ps_domains = ("akvo.akvotest3.org",
                  "cordaid.akvoapp.org",
                  "simavi.akvotest.org")
    if "host" in metafunc.funcargnames:
        metafunc.parametrize("host", hosts)
    elif "rsr_domain" in metafunc.funcargnames:
        metafunc.parametrize("rsr_domain", rsr_domains)
    elif "ps_domain" in metafunc.funcargnames:
        metafunc.parametrize("ps_domain", ps_domains)


def test_get_domain(host):
    input_host, output_host = host
    assert get_domain(FakeRequest(host=input_host)) == output_host


def test_is_rsr_instance(rsr_domain):
    assert is_rsr_instance(rsr_domain)


def test_is_partner_site_instance(ps_domain):
    assert is_partner_site_instance(ps_domain)
