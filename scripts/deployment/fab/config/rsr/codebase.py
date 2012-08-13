# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import os


class RSRCodebaseConfig(object):
    """RSRCodebaseConfig represents paths and configuration values specific to the RSR codebase"""

    UNPACKED_RSR_ARCHIVE_DIR_MASK = 'akvo-akvo-rsr-*'

    PIP_REQUIREMENTS_PATH       = 'scripts/deployment/pip/requirements'
    SYSTEM_REQUIREMENTS_FILE    = '0_system.txt'
    RSR_REQUIREMENTS_FILE       = '2_rsr.txt'
    TESTING_REQUIREMENTS_FILE   = '3_testing.txt'

    RSR_SETTINGS_HOME           = 'akvo/settings'
    LOCAL_SETTINGS_FILE         = '60-local.conf'
    LOG_FILE                    = 'akvo.log'

    RSR_MEDIA_ROOT              = 'akvo/mediaroot'

    MANAGE_SCRIPT_PATH          = 'akvo/manage.py'
    CONFIGURE_SITES_SCRIPT_PATH = 'akvo/configure_sites.py'

    RSR_APP_NAME                = 'rsr'

    def __init__(self, repository_branch):
        self.repo_branch = repository_branch
        self.repo_branch_without_type = self._branch_without_type()

        self.rsr_archive_url = os.path.join('http://nodeload.github.com/akvo/akvo-rsr/zipball', self.repo_branch)

        pip_requirements_base_url = os.path.join('https://raw.github.com/akvo/akvo-rsr', self.repo_branch, self.PIP_REQUIREMENTS_PATH)
        self.system_requirements_file_url   = os.path.join(pip_requirements_base_url, self.SYSTEM_REQUIREMENTS_FILE)
        self.rsr_requirements_file_url      = os.path.join(pip_requirements_base_url, self.RSR_REQUIREMENTS_FILE)
        self.testing_requirements_file_url  = os.path.join(pip_requirements_base_url, self.TESTING_REQUIREMENTS_FILE)

    def _branch_without_type(self):
        if self._branch_includes_type():
            return self._branch_name_only()

        return self.repo_branch

    def _branch_includes_type(self):
        return self.repo_branch.find('/') > 0

    def _branch_name_only(self):
        return self.repo_branch.split('/')[-1]
