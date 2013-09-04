# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from fab.os.linux.packageinfo import UbuntuPackageInfo


class UbuntuPackageInspector(object):

    def __init__(self, host_controller):
        self.host_controller = host_controller

    def info_for(self, package_name):
        with self.host_controller.hide_command_and_output():
            return UbuntuPackageInfo.from_text(self.host_controller.run("aptitude show %s" % package_name))

    def outdated_packages(self):
        with self.host_controller.hide_command_and_output():
            return self.host_controller.sudo("echo n | aptitude safe-upgrade")
