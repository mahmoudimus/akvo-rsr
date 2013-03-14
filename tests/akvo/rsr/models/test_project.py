# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

# from django.conf import settings

from akvo.rsr.models import Project, calculate_donation_needed_to_fully_fund

def settings_reader1(*args):
    return dict(PAYPAL_FEE_BASE_EUR=0.35, PAYPAL_FEE_PCT_EUR=3.4)

def settings_reader2(*args):
    return dict(PAYPAL_FEE_BASE_USD=0.3, PAYPAL_FEE_PCT_USD=3.9)

def settings_reader3(*args):
    return dict(MOLLIE_FEE_BASE=1.2)

def pytest_generate_tests(metafunc):
    if "donation_needed" in metafunc.funcargnames:
        metafunc.parametrize(
            ['donation_needed', 'funds_needed', 'currency', 'is_paypal', 'settings_reader'],
            [
                (104, 100, 'EUR', True, settings_reader1),
                (261, 250, 'USD', True, settings_reader2),
                (102, 100, 'EUR', False, settings_reader3),
            ]

        )

def test_calculate_donation_needed_to_fully_fund(donation_needed, funds_needed, currency, is_paypal, settings_reader):

    assert donation_needed == calculate_donation_needed_to_fully_fund(funds_needed, currency, is_paypal, settings_reader)
