# -*- coding: utf-8 -*-

import fileinput
import os

from lettuce import after, before, world
from splinter.browser import Browser

from features.smoke_tests import create_all_urls_smoke_test

world.SITE_UNDER_TEST = 'uat.akvo.org'
world.PARTNER_SITE_UNDER_TEST = 'akvo.akvotest3.org'

world.PAYPAL_MASTER_USER ='test@akvo.org'
world.PAYPAL_MASTER_PASSWORD = 'akvotest'
world.PAYPAL_TEST_USER = 'test_1352204974_per@akvo.org'
world.PAYPAL_TEST_USER_PASSWORD = 'akvotest' 
world.AKVO_ADMIN_USER = 'admintest'
world.AKVO_ADMIN_PASSWORD = 'testing123'
world.DECIMALS_DEBUG = 0 # set to 0 if this flag is not switched on in the test target (or 1 if it is)
world.PAYPAL_TEST_VISA = '4131363167241088'
world.PAYPAL_TEST_VISA_EXP_MONTH = '11'
world.PAYPAL_TEST_VISA_EXP_YEAR = '2017'

### Setup needed to run smoke_tests.create_all_urls_smoke_test()
class UrlParams(object):
    pass

url_params = UrlParams()
# "ID's" of objects to be known to exist in the RSR that is to be tested. Note that these values are not only ID's of
# objects known to exist in the DB but also any named values needed to populate a URL path in the RSR urlconf.

url_params.project_id = 276 # project_ids must be projects of the world.PARTNER_SITE_UNDER_TEST partner site
# organisation_ids must be orgs of the world.PARTNER_SITE_UNDER_TEST partner site
url_params.organisation_id = url_params.org_id = 42
url_params.donate_id = ''
url_params.update_id = 2427, 2447
url_params.slug = 'all', 'education'
url_params.cms_id = 13
url_params.iati_activity_id = 'NL-1-PPR-23872'
url_params.engine = 'paypal'
url_params.template = (
    'project-narrow', 'cobranded-narrow', 'cobranded-short', 'cobranded-banner', 'cobranded-leader', 'feature-side',
    'project-updates', 'project-contribute', 'project-small',
)
# paths we don't want to/can't test for RSR
url_params.exclude_rsr = (
    'rsr/donate/500/', 'rsr/donate/paypal/ipn/', 'rsr/maps/projects/all/json/', 'rsr/maps/organisations/all/json/',
    'rsr/accounts', 'rsr/error/access_denied/', 'rsr/rss/all-updates/', 'rsr/counter', 'rsr/notices', 'rsr/gateway',
    'rsr/api', 'api', '500/', 'rsr/media/path', 'rsr/rosetta' , 'rsr/widget/project-list/all/',
)
# paths we don't want to/can't test for partner site
# be sure to exempt all combinations of project_id and update_id for 'project/{project_id}/update/{update_id}/edit/'
url_params.exclude_ps = ('donate/thanks/', 'project/276/update/2427/edit/', 'project/276/update/2447/edit/')

world.url_params = url_params


@before.all
def setUp():
    create_all_urls_smoke_test()
    world.browser = Browser()

@after.all
def tearDown(test_results):
    world.browser.quit()

