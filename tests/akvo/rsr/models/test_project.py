# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

# from django.conf import settings

import pytest

from akvo.rsr.models import (
    calculate_donation_needed_to_fully_fund_via_paypal,
    calculate_donation_needed_to_fully_fund_via_ideal,
)

def read_settings1(*args):
    return dict(PAYPAL_FEE_BASE_EUR=0.35, PAYPAL_FEE_PCT_EUR=3.4)

def read_settings2(*args):
    return dict(PAYPAL_FEE_BASE_USD=0.3, PAYPAL_FEE_PCT_USD=3.9)

def read_settings3(*args):
    return dict(MOLLIE_FEE_BASE=1.2)

@pytest.mark.parametrize(
        ['donation_needed', 'funds_needed', 'currency', 'read_settings'],
        [
            (102, 100, 'EUR', read_settings3),
        ]
    )
def test_calculate_donation_needed_to_fully_fund_via_ideal(donation_needed, funds_needed, currency, read_settings):

    assert donation_needed == calculate_donation_needed_to_fully_fund_via_ideal(funds_needed, currency, read_settings)

@pytest.mark.parametrize(
        ['donation_needed', 'funds_needed', 'currency', 'read_settings'],
        [
            (104, 100, 'EUR', read_settings1),
            (261, 250, 'USD', read_settings2),
        ]
    )
def test_calculate_donation_needed_to_fully_fund_via_paypal(donation_needed, funds_needed, currency, read_settings):

    assert donation_needed == calculate_donation_needed_to_fully_fund_via_paypal(funds_needed, currency, read_settings)
