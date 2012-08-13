#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.tasks.environment.linux_host_base_task_test import suite as linux_host_base_task_suite
from fab.tests.tasks.environment.linux.linux_tasks_test_suite import linux_tasks_suite
from fab.tests.tasks.environment.python.python_tasks_test_suite import python_tasks_suite


def environment_tasks_suite():
    return TestSuiteLoader().create_suite_from_list([linux_host_base_task_suite(), linux_tasks_suite(), python_tasks_suite()])

if __name__ == '__main__':
    TestRunner().run_test_suite(environment_tasks_suite())
