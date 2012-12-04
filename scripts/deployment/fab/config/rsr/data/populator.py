# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import os

from fab.config.rsr.codebase import RSRCodebaseConfig
from fab.config.rsr.deployment import RSRDeploymentConfig


class RSRDataPopulatorConfig(object):

    def __init__(self, deployment_config, deployment_host_paths, codebase_config):
        self.remote_data_archives_home  = os.path.join(deployment_host_paths.deployment_processing_home, 'data_archives')
        self.local_data_archives_home   = '/var/tmp/rsr/data_archives'
        self.rsr_deployment_home        = deployment_config.rsr_deployment_home

        rsr_env_name                    = 'rsr_%s' % codebase_config.repo_branch_without_type
        self.rsr_env_path               = os.path.join(deployment_host_paths.virtualenvs_home, rsr_env_name)

        self.django_apps_to_migrate     = ['oembed', 'ipn']
        self.rsr_app_name               = RSRCodebaseConfig.RSR_APP_NAME

    @staticmethod
    def create_with(deployment_host_config):
        return RSRDataPopulatorConfig(RSRDeploymentConfig.create_with(deployment_host_config),
                                      deployment_host_config.host_paths,
                                      RSRCodebaseConfig(deployment_host_config.repository_branch))
