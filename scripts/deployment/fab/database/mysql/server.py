# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from fab.database.servercontrol import MySQLServerControl


class DatabaseServer(object):

    def __init__(self, server_control):
        self.server_control = server_control

    def is_running(self):
        return self.server_control.server_is_running()

    def shutdown(self):
        self.server_control.shutdown()

    def start(self):
        self.server_control.start()

    # or move database dir?
    def rename_database(self, database_name):
        pass

    def _response_for_command(self, command):
        admin_credentials = "--user=%s --password=%s" % (self.db_config.admin_user, self.db_config.admin_password)

        return MySQLAdminResponse(self.host_controller.sudo("mysqladmin %s %s" % (admin_credentials, command)))
