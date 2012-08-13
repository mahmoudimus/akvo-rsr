#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import mox

from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.config.spec import HostConfigSpecification
from fab.config.values.host import HostAlias
from fab.host.controller import HostControllerMode
from fab.host.database import DatabaseHost
from fab.tasks.database.migrate import RunNewDatabaseMigrations


class StubbedRunNewDatabaseMigrations(RunNewDatabaseMigrations):

    def __init__(self, database_host):
        super(StubbedRunNewDatabaseMigrations, self).__init__()
        self.configured_database_host = database_host

    def _configure_database_host_with(self, host_controller, host_config):
        return self.configured_database_host


class RunNewDatabaseMigrationsTest(mox.MoxTestBase):

    def setUp(self):
        super(RunNewDatabaseMigrationsTest, self).setUp()
        self.mock_database_host = self.mox.CreateMock(DatabaseHost)

        self.run_database_migrations_task = StubbedRunNewDatabaseMigrations(self.mock_database_host)

    def test_has_expected_task_name(self):
        """fab.tests.tasks.database.run_new_database_migrations_test  Has expected task name"""

        self.assertEqual('run_new_database_migrations', RunNewDatabaseMigrations.name)

    def test_can_run_new_database_migrations(self):
        """fab.tests.tasks.database.run_new_database_migrations_test  Can run new database migrations"""

        self.mock_database_host.run_new_migrations()
        self.mox.ReplayAll()

        self.run_database_migrations_task.run(HostControllerMode.REMOTE, HostConfigSpecification().create_preconfigured_with(HostAlias.TEST))


def suite():
    return TestSuiteLoader().load_tests_from(RunNewDatabaseMigrationsTest)

if __name__ == '__main__':
    TestRunner().run_test_suite(suite())
