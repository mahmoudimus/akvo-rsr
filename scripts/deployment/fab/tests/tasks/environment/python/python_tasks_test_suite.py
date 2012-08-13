#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.tasks.environment.python.install_python_test import suite as install_python_suite
from fab.tests.tasks.environment.python.update_system_python_packages_test import suite as python_packages_suite
from fab.tests.tasks.environment.python.virtualenv.virtualenv_tasks_test_suite import virtualenv_tasks_suite


def python_tasks_suite():
    return TestSuiteLoader().create_suite_from_list([install_python_suite(), python_packages_suite(), virtualenv_tasks_suite()])

if __name__ == '__main__':
    TestRunner().run_test_suite(python_tasks_suite())
