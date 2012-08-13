# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from fab.app.admin import DjangoAdmin
from fab.os.filesystem import FileSystem


class DjangoSettingsReader(object):

    def __init__(self, rsr_log_file_path, host_file_system, django_admin):
        self.django_admin = django_admin

        host_file_system.make_file_writable_for_all_users(rsr_log_file_path)

    @staticmethod
    def create_with(rsr_log_file_path, rsr_env_path, rsr_app_path, host_controller):
        return DjangoSettingsReader(rsr_log_file_path,
                                    FileSystem(host_controller),
                                    DjangoAdmin.create_with(rsr_env_path, rsr_app_path, host_controller))

    def rsr_database_name(self):
        return self.django_admin.read_setting('DATABASES')['default']['NAME']
