# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from akvo.rsr.models import Partnership

FIELD_PARTNER = u'field'
FUNDING_PARTNER = u'funding'
SPONSOR_PARTNER = u'sponsor'
SUPPORT_PARTNER = u'support'
ALLIANCE_PARTNER = u'alliance'
KNOWLEDGE_PARTNER = u'knowledge'
NETWORK_PARTNER = u'network'

ALL_PARTNER_TYPES = [
    FIELD_PARTNER,
    FUNDING_PARTNER,
    SPONSOR_PARTNER,
    SUPPORT_PARTNER,
    ALLIANCE_PARTNER,
    KNOWLEDGE_PARTNER,
    NETWORK_PARTNER,
]

ALL_PARTNER_TYPES_ATTR_NAMES = [
    'FIELD_PARTNER',
    'FUNDING_PARTNER',
    'SPONSOR_PARTNER',
    'SUPPORT_PARTNER',
    'ALLIANCE_PARTNER',
    'KNOWLEDGE_PARTNER',
    'NETWORK_PARTNER',
]

def pytest_generate_tests(metafunc):
    p = Partnership()
    if "partner_type_list" in metafunc.funcargnames:
        metafunc.parametrize(["partner_type_list", 'keys'],
                             [
                                 (
                                     [item[0] for item in p.PARTNER_TYPES],
                                     ALL_PARTNER_TYPES[:4]
                                 ),
                                 (
                                     [item[0] for item in p.PARTNER_TYPE_EXTRAS],
                                     ALL_PARTNER_TYPES[4:]
                                 ),
                             ]
        )
    if "attr_name" in metafunc.funcargnames:
        metafunc.parametrize(
            ['attr_name', 'attr_value'],
            zip(ALL_PARTNER_TYPES_ATTR_NAMES, ALL_PARTNER_TYPES)
        )


# testing the attributes in Partnership that defines the types of partners
def test_partnership_partner_types(attr_name, attr_value):
    partnership = Partnership()
    assert getattr(partnership, attr_name) == attr_value

def test_partnership_types_list(partner_type_list, keys):

    assert len(keys) == len(partner_type_list)

    for i, item in enumerate(partner_type_list):
        assert keys[i] == item
