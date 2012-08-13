#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import fabric.api
import mox, os

from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.helpers.feedback import ExecutionFeedback
from fab.host.controller import LocalHostController
from fab.os.command.stat import StatCommand
from fab.os.filesystem import ArchiveOptions, FileSystem, LocalFileSystem, RemoteFileSystem
from fab.os.path import PathType
from fab.os.system import SystemType


class FileSystemTest(mox.MoxTestBase):

    def setUp(self):
        super(FileSystemTest, self).setUp()
        self.mock_host_controller = self.mox.CreateMock(LocalHostController)
        self.mock_feedback = self.mox.CreateMock(ExecutionFeedback)

        self.mock_host_controller.feedback = self.mock_feedback
        self.file_system = FileSystem(self.mock_host_controller)

    def test_can_crete_localfilesystem_instance(self):
        """fab.tests.os.file_system_test  Can create a LocalFileSystem instance"""

        self.assertIsInstance(LocalFileSystem(), LocalFileSystem)

    def test_can_crete_remotefilesystem_instance(self):
        """fab.tests.os.file_system_test  Can create a RemoteFileSystem instance"""

        self.assertIsInstance(RemoteFileSystem(), RemoteFileSystem)

    def test_can_change_directory(self):
        """fab.tests.os.file_system_test  Can change directory"""

        dir_path = "/var/tmp/foo"
        changed_context = fabric.api.cd(dir_path)
        self.mock_host_controller.cd(dir_path).AndReturn(changed_context)
        self.mox.ReplayAll()

        self.assertIs(changed_context, self.file_system.cd(dir_path))

    def test_can_verify_file_existence(self):
        """fab.tests.os.file_system_test  Can verify file existence"""

        expected_file_path = "/path/to/file.txt"
        self.mock_host_controller.path_exists(expected_file_path).AndReturn(True)
        self.mox.ReplayAll()

        self.assertTrue(self.file_system.file_exists(expected_file_path), "Expected file to be found")

    def test_can_verify_directory_existence(self):
        """fab.tests.os.file_system_test  Can verify directory existence"""

        expected_dir_path = "/path/to/dir"
        self.mock_host_controller.path_exists(expected_dir_path).AndReturn(True)
        self.mox.ReplayAll()

        self.assertTrue(self.file_system.directory_exists(expected_dir_path), "Expected directory to be found")

    def test_will_exit_if_file_does_not_exist(self):
        """fab.tests.os.file_system_test  Will exit if file does not exist"""

        nonexistent_file = "/nonexistent/file.txt"
        self.mock_host_controller.path_exists(nonexistent_file).AndReturn(False)
        expected_missing_file_message = "Expected file does not exist: %s" % nonexistent_file
        self.mock_feedback.abort(expected_missing_file_message).AndRaise(SystemExit(expected_missing_file_message))
        self.mox.ReplayAll()

        with self.assertRaises(SystemExit):
            self.file_system.exit_if_file_does_not_exist(nonexistent_file)

    def test_will_confirm_file_existence_and_not_exit_if_file_exists(self):
        """fab.tests.os.file_system_test  Will confirm file existence and not exit if file exists"""

        common_system_file = "/usr/bin/man"
        self.mock_host_controller.path_exists(common_system_file).AndReturn(True)
        self.mock_feedback.comment("Found expected file: %s" % common_system_file)
        self.mox.ReplayAll()

        self.file_system.exit_if_file_does_not_exist(common_system_file)

    def test_will_exit_if_directory_does_not_exist(self):
        """fab.tests.os.file_system_test  Will exit if directory does not exist"""

        nonexistent_dir = "/nonexistent/path"
        self.mock_host_controller.path_exists(nonexistent_dir).AndReturn(False)
        expected_missing_dir_message = "Expected directory does not exist: %s" % nonexistent_dir
        self.mock_feedback.abort(expected_missing_dir_message).AndRaise(SystemExit(expected_missing_dir_message))
        self.mox.ReplayAll()

        with self.assertRaises(SystemExit):
            self.file_system.exit_if_directory_does_not_exist(nonexistent_dir)

    def test_will_confirm_directory_existence_and_not_exit_if_directory_exists(self):
        """fab.tests.os.file_system_test  Will confirm directory existence and not exit if directory exists"""

        common_system_dir = "/usr/bin"
        self.mock_host_controller.path_exists(common_system_dir).AndReturn(True)
        self.mock_feedback.comment("Found expected directory: %s" % common_system_dir)
        self.mox.ReplayAll()

        self.file_system.exit_if_directory_does_not_exist(common_system_dir)

    def test_can_create_directory(self):
        """fab.tests.os.file_system_test  Can create directory"""

        new_dir = "/var/tmp/packages"
        self._set_expectations_for_creating_directory(new_dir, with_sudo=False)

        self.file_system.create_directory(new_dir)

    def test_can_create_directory_with_sudo(self):
        """fab.tests.os.file_system_test  Can create directory with sudo"""

        new_dir = "/var/tmp/packages"
        self._set_expectations_for_creating_directory(new_dir, with_sudo=True)

        self.file_system.create_directory_with_sudo(new_dir)

    def test_will_confirm_existing_directory_when_ensuring_directory_exists(self):
        """fab.tests.os.file_system_test  Will confirm existing directory when ensuring directory exists"""

        existing_dir = "/var/tmp"
        self.mock_host_controller.path_exists(existing_dir).AndReturn(True)
        self.mock_feedback.comment("Found expected directory: %s" % existing_dir)
        self.mox.ReplayAll()

        self.file_system.ensure_directory_exists(existing_dir)

    def test_can_ensure_missing_directory_is_created(self):
        """fab.tests.os.file_system_test  Can ensure missing directory is created"""

        new_dir = "/var/tmp/packages"
        self.mock_host_controller.path_exists(new_dir).AndReturn(False)
        self._set_expectations_for_creating_directory(new_dir, with_sudo=False)

        self.file_system.ensure_directory_exists(new_dir)

    def test_will_confirm_existing_directory_when_ensuring_directory_exists_with_sudo(self):
        """fab.tests.os.file_system_test  Will confirm existing directory when ensuring directory exists with sudo"""

        existing_dir = "/var/tmp"
        self.mock_host_controller.path_exists(existing_dir).AndReturn(True)
        self.mock_feedback.comment("Found expected directory: %s" % existing_dir)
        self.mox.ReplayAll()

        self.file_system.ensure_directory_exists_with_sudo(existing_dir)

    def test_can_ensure_missing_directory_is_created_with_sudo(self):
        """fab.tests.os.file_system_test  Can ensure missing directory is created with sudo"""

        new_dir = "/var/tmp/packages"
        self.mock_host_controller.path_exists(new_dir).AndReturn(False)
        self._set_expectations_for_creating_directory(new_dir, with_sudo=True)

        self.file_system.ensure_directory_exists_with_sudo(new_dir)

    def _set_expectations_for_creating_directory(self, new_dir, with_sudo=False):
        self.mock_feedback.comment("Creating directory: %s" % new_dir)
        self._run_command("mkdir -p %s" % new_dir, with_sudo)
        self._run_command("chmod 775 %s" % new_dir, with_sudo)
        self.mox.ReplayAll()

    def test_can_create_symlink(self):
        """fab.tests.os.file_system_test  Can create a symlink"""

        self._create_symlink("/path/to/symlink", "/some/real/path", with_sudo=False)
        self.mox.ReplayAll()

        self.file_system.create_symlink("/path/to/symlink", "/some/real/path")

    def test_can_create_symlink_with_sudo(self):
        """fab.tests.os.file_system_test  Can create a symlink with sudo"""

        self._create_symlink("/path/to/symlink", "/some/real/path", with_sudo=True)
        self.mox.ReplayAll()

        self.file_system.create_symlink("/path/to/symlink", "/some/real/path", with_sudo=True)

    def _create_symlink(self, symlink_path, real_path, with_sudo):
        self._run_command("ln -s %s %s" % (real_path, symlink_path), with_sudo)
        self._linked_path_for_symlink(symlink_path, real_path)
        self.mock_feedback.comment("Created symlink: %s -> %s" % (symlink_path, real_path))

    def test_can_remove_symlink(self):
        """fab.tests.os.file_system_test  Can remove a symlink"""

        self._remove_symlink("/path/to/symlink", with_sudo=False)
        self.mox.ReplayAll()

        self.file_system.remove_symlink("/path/to/symlink")

    def test_can_remove_symlink_with_sudo(self):
        """fab.tests.os.file_system_test  Can remove a symlink with sudo"""

        self._remove_symlink("/path/to/symlink", with_sudo=True)
        self.mox.ReplayAll()

        self.file_system.remove_symlink("/path/to/symlink", with_sudo=True)

    def _remove_symlink(self, symlink_path, with_sudo):
        self.mock_feedback.comment("Removing symlink: /path/to/symlink")
        self._run_command("unlink /path/to/symlink", with_sudo)

    def test_will_abort_if_attempting_to_ensure_existence_of_existing_non_symlink_path(self):
        """fab.tests.os.file_system_test  Will abort if attempting to ensure existence of an existing non-symlink path"""

        self.mock_host_controller.path_exists("/path/to/dir").AndReturn(True)
        self._set_expected_path_type(PathType.DIRECTORY, "/path/to/dir")
        self.mock_feedback.abort("Found existing path but path is not a symlink: /path/to/dir")
        self.mox.ReplayAll()

        self.file_system.ensure_symlink_exists("/path/to/dir", "/some/real/path")

    def test_will_abort_if_attempting_to_create_broken_symlink(self):
        """fab.tests.os.file_system_test  Will abort if attempting to create a broken symlink"""

        self.mock_host_controller.path_exists("/path/to/symlink").AndReturn(False)
        self.mock_host_controller.path_exists("/some/nonexistent/path").AndReturn(False)
        self.mock_feedback.abort("Cannot create symlink to nonexistent path: /some/nonexistent/path")
        self.mox.ReplayAll()

        self.file_system.ensure_symlink_exists("/path/to/symlink", "/some/nonexistent/path")

    def test_will_acknowledge_existing_valid_symlink_when_attempting_to_ensure_symlink_exists(self):
        """fab.tests.os.file_system_test  Will acknowledge existing valid symlink when attempting to ensure symlink exists"""

        self.mock_host_controller.path_exists("/path/to/symlink").AndReturn(True)
        self._set_expected_path_type(PathType.SYMLINK, "/path/to/symlink")
        self.mock_host_controller.path_exists("/some/real/path").AndReturn(True)
        self.mock_host_controller.path_exists("/path/to/symlink").AndReturn(True)
        self._linked_path_for_symlink("/path/to/symlink", "/some/real/path")
        self._linked_path_for_symlink("/path/to/symlink", "/some/real/path")
        self.mock_feedback.comment("Found expected symlink: /path/to/symlink -> /some/real/path")
        self.mox.ReplayAll()

        self.file_system.ensure_symlink_exists("/path/to/symlink", "/some/real/path")

    def test_can_ensure_symlink_exists_by_relinking_to_expected_real_path(self):
        """fab.tests.os.file_system_test  Can ensure symlink exists by relinking to the expected real path"""

        self.mock_host_controller.path_exists("/path/to/symlink").AndReturn(True)
        self._set_expected_path_type(PathType.SYMLINK, "/path/to/symlink")
        self.mock_host_controller.path_exists("/some/real/path").AndReturn(True)
        self.mock_host_controller.path_exists("/path/to/symlink").AndReturn(True)
        self._linked_path_for_symlink("/path/to/symlink", "/another/path")
        self.mock_host_controller.path_exists("/path/to/symlink").AndReturn(True)
        self._remove_symlink("/path/to/symlink", with_sudo=False)
        self._create_symlink("/path/to/symlink", "/some/real/path", with_sudo=False)
        self.mox.ReplayAll()

        self.file_system.ensure_symlink_exists("/path/to/symlink", "/some/real/path")

    def _linked_path_for_symlink(self, symlink_path, expected_path):
        self.mock_host_controller.hide_command_and_output().AndReturn(fabric.api.hide('running', 'stdout'))
        self.mock_host_controller.run("readlink %s" % symlink_path).AndReturn(expected_path)

    def test_can_ensure_symlink_exists_by_creating_missing_symlink(self):
        """fab.tests.os.file_system_test  Can ensure symlink exists by creating a missing symlink"""

        self.mock_host_controller.path_exists("/path/to/symlink").AndReturn(False)
        self.mock_host_controller.path_exists("/some/real/path").AndReturn(True)
        self.mock_host_controller.path_exists("/path/to/symlink").MultipleTimes().AndReturn(False)
        self._create_symlink("/path/to/symlink", "/some/real/path", with_sudo=False)
        self.mox.ReplayAll()

        self.file_system.ensure_symlink_exists("/path/to/symlink", "/some/real/path")

    def _set_expected_path_type(self, path_type, path):
        self.mock_host_controller.hide_command_and_output().AndReturn(fabric.api.hide('running', 'stdout'))
        self.mock_host_controller.run("uname -s").AndReturn(SystemType.LINUX)
        self.mock_host_controller.hide_command_and_output().AndReturn(fabric.api.hide('running', 'stdout'))
        self.mock_host_controller.run(StatCommand(SystemType.LINUX).for_path(path)).AndReturn(path_type)

    def test_can_rename_file(self):
        """fab.tests.os.file_system_test  Can rename a file"""

        original_file = "/var/tmp/original/file.txt"
        new_file = "/var/tmp/something/else.txt"
        self.mock_host_controller.run("mv %s %s" % (original_file, new_file))
        self.mox.ReplayAll()

        self.file_system.rename_file(original_file, new_file)

    def test_can_rename_directory(self):
        """fab.tests.os.file_system_test  Can rename a directory"""

        original_dir = "/var/tmp/original"
        new_dir = "/var/tmp/something/else"
        self.mock_host_controller.run("mv %s %s" % (original_dir, new_dir))
        self.mox.ReplayAll()

        self.file_system.rename_directory(original_dir, new_dir)

    def test_can_make_file_writable_for_all_users(self):
        """fab.tests.os.file_system_test  Can make file writable for all users"""

        file_path = "/var/tmp/file_to_change.txt"
        self.mock_host_controller.sudo("chmod a+w %s" % file_path)
        self.mox.ReplayAll()

        self.file_system.make_file_writable_for_all_users(file_path)

    def test_can_delete_an_existing_file(self):
        """fab.tests.os.file_system_test  Can delete an existing file"""

        unwanted_file = "/var/tmp/unwanted_file.txt"
        self._set_expectations_for_deleting("file", unwanted_file, self.mock_host_controller.run)

        self.file_system.delete_file(unwanted_file)

    def test_can_delete_an_existing_file_with_sudo(self):
        """fab.tests.os.file_system_test  Can delete an existing file with sudo"""

        unwanted_file = "/var/tmp/unwanted_file.txt"
        self._set_expectations_for_deleting("file", unwanted_file, self.mock_host_controller.sudo)

        self.file_system.delete_file_with_sudo(unwanted_file)

    def test_do_nothing_on_attempt_to_delete_a_nonexistent_file(self):
        """fab.tests.os.file_system_test  Do nothing on attempt to delete a nonexistent file"""

        nonexistent_file = "/var/tmp/wibble.txt"
        self.mock_host_controller.path_exists(nonexistent_file).AndReturn(False)
        self.mox.ReplayAll()

        self.file_system.delete_file(nonexistent_file)

    def test_do_nothing_on_attempt_to_delete_a_nonexistent_file_with_sudo(self):
        """fab.tests.os.file_system_test  Do nothing on attempt to delete a nonexistent file with sudo"""

        nonexistent_file = "/var/tmp/wibble.txt"
        self.mock_host_controller.path_exists(nonexistent_file).AndReturn(False)
        self.mox.ReplayAll()

        self.file_system.delete_file_with_sudo(nonexistent_file)

    def test_can_delete_an_existing_directory(self):
        """fab.tests.os.file_system_test  Can delete an existing directory"""

        unwanted_dir = "/var/tmp/unwanted_dir"
        self._set_expectations_for_deleting("directory", unwanted_dir, self.mock_host_controller.run)

        self.file_system.delete_directory(unwanted_dir)

    def test_can_delete_an_existing_directory_with_sudo(self):
        """fab.tests.os.file_system_test  Can delete an existing directory with sudo"""

        unwanted_dir = "/var/tmp/unwanted_dir"
        self._set_expectations_for_deleting("directory", unwanted_dir, self.mock_host_controller.sudo)

        self.file_system.delete_directory_with_sudo(unwanted_dir)

    def test_do_nothing_on_attempt_to_delete_a_nonexistent_directory(self):
        """fab.tests.os.file_system_test  Do nothing on attempt to delete a nonexistent directory"""

        nonexistent_dir = "/var/tmp/wibble_dir"
        self.mock_host_controller.path_exists(nonexistent_dir).AndReturn(False)
        self.mox.ReplayAll()

        self.file_system.delete_directory(nonexistent_dir)

    def test_do_nothing_on_attempt_to_delete_a_nonexistent_directory_with_sudo(self):
        """fab.tests.os.file_system_test  Do nothing on attempt to delete a nonexistent directory with sudo"""

        nonexistent_dir = "/var/tmp/wibble_dir"
        self.mock_host_controller.path_exists(nonexistent_dir).AndReturn(False)
        self.mox.ReplayAll()

        self.file_system.delete_directory_with_sudo(nonexistent_dir)

    def _set_expectations_for_deleting(self, file_or_dir, unwanted_file_or_dir_path, expected_run_command):
        self.mock_host_controller.path_exists(unwanted_file_or_dir_path).AndReturn(True)
        self.mock_feedback.comment(mox.StrContains("Deleting %s: %s" % (file_or_dir, unwanted_file_or_dir_path)))
        expected_run_command("rm -r %s" % unwanted_file_or_dir_path)
        self.mox.ReplayAll()

    def test_can_decompress_code_archive(self):
        """fab.tests.os.file_system_test  Can decompress a code archive"""

        self._decompress_archive("/path/to/rsr_code.zip", "/some/destination/dir", "-x %s" % ArchiveOptions.CODE_ARCHIVE_EXCLUSIONS)

        self.file_system.decompress_code_archive("/path/to/rsr_code.zip", "/some/destination/dir")

    def test_can_decompress_data_archive(self):
        """fab.tests.os.file_system_test  Can decompress a data archive"""

        self._decompress_archive("/path/to/rsr_data.zip", "/some/destination/dir", ArchiveOptions.NONE)

        self.file_system.decompress_data_archive("/path/to/rsr_data.zip", "/some/destination/dir")

    def _decompress_archive(self, expected_archive_file_name, expected_destination_dir, expected_options):
        self.mock_host_controller.run("unzip -q %s -d %s %s".rstrip() % (expected_archive_file_name,
                                                                         expected_destination_dir,
                                                                         expected_options))
        self.mox.ReplayAll()

    def test_can_compress_directory(self):
        """fab.tests.os.file_system_test  Can compress a specified directory"""

        dir_to_compress = "/var/archives/data_4423"
        expected_parent_dir = "/var/archives"
        expected_archive_file = "data_4423.zip"
        self._compress_resource(dir_to_compress, expected_parent_dir, expected_archive_file)

        self.file_system.compress_directory(dir_to_compress)

    def test_can_compress_directory_with_trailing_path_separator(self):
        """fab.tests.os.file_system_test  Can compress a specified directory even with a trailing path separator"""

        dir_to_compress = "/var/archives/data_4423/"
        expected_parent_dir = "/var/archives"
        expected_archive_file = "data_4423.zip"
        self._compress_resource(dir_to_compress.rstrip("/"), expected_parent_dir, expected_archive_file)

        self.file_system.compress_directory(dir_to_compress)

    def _compress_resource(self, resource_path, expected_parent_dir, expected_archive_file):
        self.mock_feedback.comment("Compressing %s" % resource_path)
        self._change_dir_to(expected_parent_dir)
        expected_archive_name = expected_archive_file.replace(".zip", "")
        self.mock_host_controller.run("zip -r %s %s" % (expected_archive_file, expected_archive_name))
        self.mox.ReplayAll()

    def test_can_download_file(self):
        """fab.tests.os.file_system_test  Can download a file"""

        host_file_path = "/var/some/dir/file.zip"
        local_directory = "/var/tmp/archives"

        self.mock_host_controller.get(host_file_path, local_directory)
        self.mox.ReplayAll()

        self.file_system.download_file(host_file_path, local_directory)

    def test_can_upload_file(self):
        """fab.tests.os.file_system_test  Can upload a file"""

        local_file_path = "/var/some/local/file.zip"
        remote_directory = "/var/tmp/archives"

        self.mock_host_controller.put(local_file_path, remote_directory, mirror_local_mode=True)
        self.mox.ReplayAll()

        self.file_system.upload_file(local_file_path, remote_directory)

    def test_can_get_most_recent_file_in_directory(self):
        """fab.tests.os.file_system_test  Can get most recent file in a directory"""

        self.mock_host_controller.run("ls -1tr /var/some/dir | tail -1")
        self.mox.ReplayAll()

        self.file_system.most_recent_file_in_directory("/var/some/dir")

    def _run_command(self, command, with_sudo=False):
        return self.mock_host_controller.sudo(command) if with_sudo else self.mock_host_controller.run(command)

    def _change_dir_to(self, expected_dir):
        self.mock_host_controller.cd(expected_dir).AndReturn(fabric.api.cd(expected_dir))


def suite():
    return TestSuiteLoader().load_tests_from(FileSystemTest)

if __name__ == '__main__':
    TestRunner().run_test_suite(suite())
