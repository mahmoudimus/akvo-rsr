#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.host.data_retrieval_host_test import DataRetrievalHostTest
from fab.tests.host.database_host_test import DatabaseHostTest
from fab.tests.host.deployment_host_test import DeploymentHostTest
from fab.tests.host.host_controller_mode_test import HostControllerModeTest
from fab.tests.host.host_controller_test import HostControllerTest
from fab.tests.host.linux_host_test import LinuxHostTest
from fab.tests.host.local_host_controller_test import LocalHostControllerTest
from fab.tests.host.neutral_host_test import NeutralHostTest
from fab.tests.host.remote_host_controller_test import RemoteHostControllerTest
from fab.tests.host.virtualenv_deployment_host_test import VirtualEnvDeploymentHostTest


def host_suite():
    return TestSuiteLoader().create_suite_from_classes([HostControllerModeTest, HostControllerTest,
                                                        LocalHostControllerTest, RemoteHostControllerTest,
                                                        LinuxHostTest, NeutralHostTest, DataRetrievalHostTest,
                                                        DatabaseHostTest, DeploymentHostTest,
                                                        VirtualEnvDeploymentHostTest])

if __name__ == '__main__':
    TestRunner().run_test_suite(host_suite())
