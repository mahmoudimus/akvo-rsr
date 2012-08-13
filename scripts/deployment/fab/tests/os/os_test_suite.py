#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.os.akvo_permissions_test import suite as permissions_suite
from fab.tests.os.command.os_command_test_suite import os_command_suite
from fab.tests.os.file_system_test import suite as file_system_suite
from fab.tests.os.linux.linux_test_suite import linux_suite
from fab.tests.os.path_info_test import suite as path_info_suite
from fab.tests.os.path_type_test import suite as path_type_suite
from fab.tests.os.symlink_info_test import suite as symlink_info_suite
from fab.tests.os.system_info_test import suite as system_info_suite


def os_suite():
    return TestSuiteLoader().create_suite_from_list([system_info_suite(), path_type_suite(), path_info_suite(),
                                                     symlink_info_suite(), os_command_suite(), file_system_suite(),
                                                     permissions_suite(), linux_suite()])

if __name__ == '__main__':
    TestRunner().run_test_suite(os_suite())
