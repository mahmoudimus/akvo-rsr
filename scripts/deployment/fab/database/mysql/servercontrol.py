# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from fab.config.rsr.database import RSRDatabaseConfig
from fab.os.filesystem import FileSystem


class MySQLInstallation(object):

    class Linux(object):

        CONTROLLER_PATH = "/etc/init.d/mysqld"
        START_COMMAND   = "%s start" % CONTROLLER_PATH

    class Community(object):

        CONTROLLER_PATH = "/Library/StartupItems/MySQLCOM/MySQLCOM"
        START_COMMAND   = "%s start" % CONTROLLER_PATH

    class Homebrew(object):

        CONTROLLER_PATH = "~/Library/LaunchAgents/com.mysql.mysqld.plist"
        START_COMMAND   = "launchctl load %s" % CONTROLLER_PATH


class MySQLServerControl(object):

    installation_types = { MySQLInstallation.Linux, MySQLInstallation.Community, MySQLInstallation.Homebrew }

    def __init__(self, database_config, file_system, host_controller):
        self.admin_credentials = "--user=%s --password=%s" % (database_config.admin_user, database_config.admin_password)
        self.host_controller = host_controller
        self.feedback = host_controller.feedback

        self.start_command = self._determine_start_command(file_system)

    def _determine_start_command(self, file_system):
        return filter(lambda installation: file_system.file_exists(installation.CONTROLLER_PATH), self.installation_types)[0].START_COMMAND

    @staticmethod
    def create_instance(host_controller):
        return MySQLServerControl(RSRDatabaseConfig.from_local_config_values())

    def server_is_running(self):
        try:
            if self._response_for("ping").server_is_alive():
                self.feedback.comment("MySQL server is running")
                return True
        except Exception:
            self.feedback.comment("MySQL server not running")
            return False

    def shutdown(self):
        if self.server_is_running():
            self.feedback.comment("Shutting down MySQL server")
            self._execute_command("shutdown")
        else:
            self.feedback.comment("MySQL server already shutdown")

    def start(self):
        if self.server_is_running():
            self.feedback.comment("Starting MySQL server")
            self.host_controller.sudo(self.start_command)
        else:
            self.feedback.comment("MySQL server already started")

        self._execute_command("status")

    def _response_for(self, command):
        return MySQLAdminResponse(self._execute_command(command))

    def _execute_command(self, command):
        return self.host_controller.sudo("mysqladmin %s %s" % (self.admin_credentials, command))


class MySQLAdminResponse(object):

    def __init__(self, mysqladmin_response_text):
        self.admin_response_text = mysqladmin_response_text

    def server_is_alive(self):
        return self._response_contains("is alive")

    def _response_contains(self, text):
        return self.admin_response_text.find(text) >= 0
