#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import mox

from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.app.admin import DjangoAdmin
from fab.app.settings import DjangoSettingsReader
from fab.host.controller import LocalHostController, RemoteHostController
from fab.helpers.feedback import ExecutionFeedback
from fab.os.filesystem import FileSystem


class DjangoSettingsReaderTest(mox.MoxTestBase):

    def setUp(self):
        super(DjangoSettingsReaderTest, self).setUp()
        self.mock_host_file_system = self.mox.CreateMock(FileSystem)
        self.mock_django_admin = self.mox.CreateMock(DjangoAdmin)

        self.rsr_log_file_path = '/path/to/rsr.log'

    def test_can_create_instance_for_local_host(self):
        """fab.tests.app.settings.django_settings_reader_test  Can create DjangoSettingsReader instance for local host"""

        self._can_create_instance_for(LocalHostController)

    def test_can_create_instance_for_remote_host(self):
        """fab.tests.app.settings.django_settings_reader_test  Can create DjangoSettingsReader instance for remote host"""

        self._can_create_instance_for(RemoteHostController)

    def _can_create_instance_for(self, host_controller_class):
        rsr_env_path = '/path/to/rsr/env'
        rsr_app_path = '/path/to/rsr/app'

        mock_host_controller = self.mox.CreateMock(host_controller_class)
        mock_host_controller.feedback = self.mox.CreateMock(ExecutionFeedback)
        mock_host_controller.sudo('chmod a+w %s' % self.rsr_log_file_path)
        self.mox.ReplayAll()

        self.assertIsInstance(DjangoSettingsReader.create_with(self.rsr_log_file_path, rsr_env_path, rsr_app_path, mock_host_controller),
                              DjangoSettingsReader)

    def test_initialiser_ensures_log_file_is_writable_before_reading_settings(self):
        """fab.tests.app.settings.django_settings_reader_test  Initialiser ensures log file is writable before reading settings"""

        self._make_log_file_writable()
        self.mox.ReplayAll()

        self._create_settings_reader()

    def test_can_read_rsr_database_name(self):
        """fab.tests.app.settings.django_settings_reader_test  Can read RSR database name"""

        deployed_database_settings = { 'default': { 'NAME': 'some_rsrdb' } }

        self._make_log_file_writable()
        self.mock_django_admin.read_setting('DATABASES').AndReturn(deployed_database_settings)
        self.mox.ReplayAll()

        settings_reader = self._create_settings_reader()

        self.assertEqual('some_rsrdb', settings_reader.rsr_database_name())

    def _make_log_file_writable(self):
        self.mock_host_file_system.make_file_writable_for_all_users(self.rsr_log_file_path)

    def _create_settings_reader(self):
        return DjangoSettingsReader(self.rsr_log_file_path, self.mock_host_file_system, self.mock_django_admin)


def suite():
    return TestSuiteLoader().load_tests_from(DjangoSettingsReaderTest)

if __name__ == '__main__':
    TestRunner().run_test_suite(suite())
