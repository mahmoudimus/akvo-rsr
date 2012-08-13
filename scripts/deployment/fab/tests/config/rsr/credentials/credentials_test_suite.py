#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.config.rsr.credentials.credentials_file_reader_test import CredentialsFileReaderTest
from fab.tests.config.rsr.credentials.custom_user_credentials_test import CustomUserCredentialsTest
from fab.tests.config.rsr.credentials.database_credentials_test import DatabaseCredentialsTest
from fab.tests.config.rsr.credentials.user_credentials_test import UserCredentialsTest


def credentials_suite():
    return TestSuiteLoader().create_suite_from_classes([CredentialsFileReaderTest, CustomUserCredentialsTest,
                                                        DatabaseCredentialsTest, UserCredentialsTest])

if __name__ == '__main__':
    TestRunner().run_test_suite(credentials_suite())
