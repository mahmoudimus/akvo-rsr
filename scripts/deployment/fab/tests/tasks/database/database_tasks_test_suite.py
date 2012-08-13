#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.tasks.database.backup_rsr_database_test import BackupRSRDatabaseTest
from fab.tests.tasks.database.rebuild_rsr_database_test import RebuildRSRDatabaseTest
from fab.tests.tasks.database.rsr_database_task_test import RSRDatabaseTaskTest
from fab.tests.tasks.database.run_new_database_migrations_test import RunNewDatabaseMigrationsTest


def database_tasks_suite():
    return TestSuiteLoader().create_suite_from_classes([BackupRSRDatabaseTest, RebuildRSRDatabaseTest,
                                                        RSRDatabaseTaskTest, RunNewDatabaseMigrationsTest])

if __name__ == '__main__':
    TestRunner().run_test_suite(database_tasks_suite())
