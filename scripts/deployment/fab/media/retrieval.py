# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import os

from fab.config.rsr.media.retrieval import RSRMediaRetrieverConfig
from fab.format.timestamp import TimeStampFormatter
from fab.host.controller import RemoteHostController
from fab.os.filesystem import FileSystem


class RSRMediaRetriever(object):

    def __init__(self, media_retriever_config, file_system, time_stamp_formatter, feedback):
        self.config = media_retriever_config
        self.file_system = file_system
        self.time_stamp_formatter = time_stamp_formatter
        self.feedback = feedback

    @staticmethod
    def create_instance():
        host_controller = RemoteHostController.create_instance()

        return RSRMediaRetriever(RSRMediaRetrieverConfig.create_instance(),
                                 FileSystem(host_controller),
                                 TimeStampFormatter(),
                                 host_controller.feedback)

    def fetch_latest_media_archive(self):
        self._ensure_required_paths_exist()
        self._compress_and_download_media_archive()

    def _ensure_required_paths_exist(self):
        self.file_system.ensure_directory_exists(self.config.media_archives_home)
        self.exit_if_directory_does_not_exist(self.config.rsr_media_snapshot_path)

    def _compress_and_download_media_archive(self):
        self.file_system.compress_directory(self.config.rsr_media_snapshot_path)
        self.file_system.move_file()            

    # def time_stamped_path_for(self, snapshot_path):
    #     return self.time_stamp_formatter.append_timestamp(snapshot_path)
