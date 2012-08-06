#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import os, unittest2

from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.config.rsr.codebase import RSRCodebaseConfig
from fab.config.rsr.deployment import RSRDeploymentConfig
from fab.config.rsr.host import CIDeploymentHostConfig


class RSRDeploymentConfigTest(unittest2.TestCase):

    def setUp(self):
        super(RSRDeploymentConfigTest, self).setUp()

        self.deployment_user = 'rupaul'
        self.deployment_host_config = CIDeploymentHostConfig.for_test()
        self.deployment_host_paths = self.deployment_host_config.host_paths
        self.codebase_config = RSRCodebaseConfig(self.deployment_host_config.repository_branch)

        self.expected_rsr_dir_name = 'rsr_%s' % self.codebase_config.repo_branch_without_type
        self.expected_rsr_deployment_home = os.path.join(self.deployment_host_paths.repo_checkout_home, self.expected_rsr_dir_name)
        self.expected_current_virtualenv_path = os.path.join(self.deployment_host_paths.virtualenvs_home, 'current')

        self.deployment_config = RSRDeploymentConfig(self.deployment_host_paths, self.deployment_user, self.codebase_config)

    def test_can_create_rsrdeploymentconfig_instance(self):
        """fab.tests.config.rsr.deployment_config_test  Can create RSRDeploymentConfig instance"""

        self.assertIsInstance(RSRDeploymentConfig.create_with(self.deployment_host_config, self.deployment_user), RSRDeploymentConfig)
        self.assertIsInstance(RSRDeploymentConfig.create_with(self.deployment_host_config), RSRDeploymentConfig)

    def test_has_deployment_user_name(self):
        """fab.tests.config.rsr.deployment_config_test  Has deployment user name"""

        self.assertEqual(self.deployment_user, self.deployment_config.deployment_user)

    def test_has_repository_checkout_home(self):
        """fab.tests.config.rsr.deployment_config_test  Has repository checkout home"""

        self.assertEqual(self.deployment_host_paths.repo_checkout_home, self.deployment_config.repo_checkout_home)

    def test_has_repository_archives_directory(self):
        """fab.tests.config.rsr.deployment_config_test  Has repository archives directory"""

        expected_repo_archives_dir = os.path.join(self.deployment_host_paths.repo_checkout_home, 'archives')

        self.assertEqual(expected_repo_archives_dir, self.deployment_config.repo_archives_dir)

    def test_has_rsr_code_archive_url(self):
        """fab.tests.config.rsr.deployment_config_test  Has RSR code archive URL"""

        self.assertEqual(self.codebase_config.rsr_archive_url, self.deployment_config.rsr_archive_url)

    def test_has_unpacked_archive_directory_mask(self):
        """fab.tests.config.rsr.deployment_config_test  Has unpacked archive directory mask"""

        self.assertEqual(RSRCodebaseConfig.UNPACKED_RSR_ARCHIVE_DIR_MASK, self.deployment_config.unpacked_archive_dir_mask)

    def test_has_rsr_deployment_directory_name(self):
        """fab.tests.config.rsr.deployment_config_test  Has RSR deployment directory name"""

        self.assertEqual(self.expected_rsr_dir_name, self.deployment_config.rsr_deployment_dir_name)

    def test_has_rsr_deployment_home(self):
        """fab.tests.config.rsr.deployment_config_test  Has RSR deployment home"""

        self.assertEqual(self.expected_rsr_deployment_home, self.deployment_config.rsr_deployment_home)

    def test_has_rsr_settings_home(self):
        """fab.tests.config.rsr.deployment_config_test  Has RSR settings home"""

        expected_rsr_settings_home = os.path.join(self.expected_rsr_deployment_home, RSRCodebaseConfig.RSR_SETTINGS_HOME)

        self.assertEqual(expected_rsr_settings_home, self.deployment_config.rsr_settings_home)

    def test_has_rsr_media_root(self):
        """fab.tests.config.rsr.deployment_config_test  Has RSR media root"""

        expected_rsr_media_root = os.path.join(self.expected_rsr_deployment_home, RSRCodebaseConfig.RSR_MEDIA_ROOT)

        self.assertEqual(expected_rsr_media_root, self.deployment_config.rsr_media_root)

    def test_has_current_rsr_media_root(self):
        """fab.tests.config.rsr.deployment_config_test  Has current RSR media root"""

        expected_current_rsr_media_root = os.path.join(self.deployment_config.repo_checkout_home, 'current', RSRCodebaseConfig.RSR_MEDIA_ROOT)

        self.assertEqual(expected_current_rsr_media_root, self.deployment_config.current_rsr_media_root)

    def test_has_current_virtualenv_path(self):
        """fab.tests.config.rsr.deployment_config_test  Has current virtualenv path"""

        self.assertEqual(self.expected_current_virtualenv_path, self.deployment_config.current_virtualenv_path)

    def test_has_django_media_admin_path(self):
        """fab.tests.config.rsr.deployment_config_test  Has Django media admin path"""

        expected_django_media_admin_path = os.path.join(self.expected_current_virtualenv_path, RSRDeploymentConfig.DJANGO_LIB_PATH, 'contrib/admin/static/admin')

        self.assertEqual(expected_django_media_admin_path, self.deployment_config.django_media_admin_path)

    def test_has_rsr_static_media_home(self):
        """fab.tests.config.rsr.deployment_config_test  Has RSR static media home"""

        self.assertEqual(os.path.join(self.deployment_host_paths.static_media_home, 'akvo'), self.deployment_config.rsr_static_media_home)

    def test_has_static_media_db_path(self):
        """fab.tests.config.rsr.deployment_config_test  Has static media DB path"""

        self.assertEqual(os.path.join(self.deployment_host_paths.static_media_home, 'akvo/db'), self.deployment_config.static_media_db_path)

    def test_has_host_config_home(self):
        """fab.tests.config.rsr.deployment_config_test  Has host configuration home"""

        self.assertEqual(self.deployment_host_paths.config_home, self.deployment_config.host_config_home)

    def test_has_local_rsr_settings_file_name(self):
        """fab.tests.config.rsr.deployment_config_test  Has local RSR settings file name"""

        self.assertEqual(RSRCodebaseConfig.LOCAL_SETTINGS_FILE, self.deployment_config.local_rsr_settings_file_name)

    def test_has_deployed_rsr_settings_file_path(self):
        """fab.tests.config.rsr.deployment_config_test  Has deployed RSR settings file path"""

        expected_deployed_settings_file_path = os.path.join(self.deployment_host_paths.config_home, RSRCodebaseConfig.LOCAL_SETTINGS_FILE)

        self.assertEqual(expected_deployed_settings_file_path, self.deployment_config.deployed_rsr_settings_file)

    def test_has_log_file_path(self):
        """fab.tests.config.rsr.deployment_config_test  Has RSR log file path"""

        expected_log_file_path = os.path.join(self.deployment_host_paths.logging_home, RSRCodebaseConfig.LOG_FILE)

        self.assertEqual(expected_log_file_path, self.deployment_config.log_file_path)


def suite():
    return TestSuiteLoader().load_tests_from(RSRDeploymentConfigTest)

if __name__ == '__main__':
    TestRunner().run_test_suite(suite())
