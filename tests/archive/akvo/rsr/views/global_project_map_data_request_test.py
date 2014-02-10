#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import unittest

from django.core.management import setup_environ
import akvo.settings
setup_environ(akvo.settings)

from testing.helpers.execution import TestRunner, TestSuiteLoader

from akvo.rsr.views import global_project_map_json


class GlobalProjectMapDataRequestTest(unittest.TestCase):

    def test_can_get_data_for_global_project_map(self):
        """rsr.views.maps.global_project_map_json_request_test  Can get data for global project map"""

        expected_response = []
        self.assertEqual(expected_response, global_project_map_json(None))
        self.fail('in progress')


def suite():
    return TestSuiteLoader().load_tests_from(GlobalProjectMapDataRequestTest)

if __name__ == '__main__':
    TestRunner().run_test_suite(suite())
