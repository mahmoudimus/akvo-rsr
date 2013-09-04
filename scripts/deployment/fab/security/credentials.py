# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import os

from fab.verifiers.config import ConfigFileVerifier


class CredentialsInstaller(object):

    def __init__(self, config_file_verifier, file_crypter):
        self.config_file_verifier = config_file_verifier
        self.file_crypter = file_crypter

    def install_database_credentials(self):
        self.config_file_verifier.exit_if_database_credentials_not_found()


class SimpleLoginCredentials(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password


class ServerLoginCredentials(SimpleLoginCredentials):

    def __init__(self, server_name, user, password):
        super(ServerLoginCredentials, self).__init__(user, password)
        self.server_name = server_name
