#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.os.linux.ubuntu_package_info_test import UbuntuPackageInfoTest
from fab.tests.os.linux.ubuntu_package_inspector_test import UbuntuPackageInspectorTest


def linux_suite():
    return TestSuiteLoader().create_suite_from_classes([UbuntuPackageInspectorTest, UbuntuPackageInfoTest])

if __name__ == '__main__':
    TestRunner().run_test_suite(linux_suite())
