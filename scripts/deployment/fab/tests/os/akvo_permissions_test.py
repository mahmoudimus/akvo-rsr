#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


import mox

from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.helpers.feedback import ExecutionFeedback
from fab.host.controller import RemoteHostController
from fab.os.permissions import AkvoPermissions


class AkvoPermissionsTest(mox.MoxTestBase):

    def setUp(self):
        super(AkvoPermissionsTest, self).setUp()
        self.mock_host_controller = self.mox.CreateMock(RemoteHostController)
        self.mock_feedback = self.mox.CreateMock(ExecutionFeedback)

        self.mock_host_controller.feedback = self.mock_feedback
        self.permissions = AkvoPermissions(self.mock_host_controller)

    def test_will_confirm_if_user_has_sudo_permission(self):
        """fab.tests.os.akvo_permissions_test  Will confirm if user has sudo permission"""

        self.mock_host_controller.run("groups joesoap").AndReturn("joesoap accounts admin everyone writers")
        self.mock_feedback.comment("User [joesoap] has expected sudo permission through membership of the [admin] group")
        self.mox.ReplayAll()

        self.permissions.exit_if_user_does_not_have_sudo_permission("joesoap")

    def test_exit_if_user_does_not_have_sudo_permission(self):
        """fab.tests.os.akvo_permissions_test  Exit if the user does not have sudo permission"""

        self.mock_host_controller.run("groups joesoap").AndReturn("joesoap accounts everyone writers")
        expected_user_not_in_group_message = "User [joesoap] should have sudo permission through membership of the [admin] group"
        self.mock_feedback.abort(expected_user_not_in_group_message).AndRaise(SystemExit(expected_user_not_in_group_message))
        self.mox.ReplayAll()

        with self.assertRaises(SystemExit):
            self.permissions.exit_if_user_does_not_have_sudo_permission("joesoap")

    def test_will_confirm_group_membership_if_user_is_member_of_web_group(self):
        """fab.tests.os.akvo_permissions_test  Will confirm group membership if user is a member of the web user group"""

        self.mock_host_controller.run("groups joesoap").AndReturn("joesoap accounts everyone %s" % AkvoPermissions.WEB_USER_GROUP)
        self.mock_feedback.comment("User [joesoap] is a member of expected group [%s]" % AkvoPermissions.WEB_USER_GROUP)
        self.mox.ReplayAll()

        self.permissions.exit_if_user_is_not_member_of_web_group("joesoap")

    def test_exit_if_user_is_not_a_member_of_web_group(self):
        """fab.tests.os.akvo_permissions_test  Exit if the user is not a member of the web user group"""

        self.mock_host_controller.run("groups joesoap").AndReturn("joesoap accounts everyone writers")
        expected_user_not_in_group_message = "User [joesoap] should be a member of group [%s]" % AkvoPermissions.WEB_USER_GROUP
        self.mock_feedback.abort(expected_user_not_in_group_message).AndRaise(SystemExit(expected_user_not_in_group_message))
        self.mox.ReplayAll()

        with self.assertRaises(SystemExit):
            self.permissions.exit_if_user_is_not_member_of_web_group("joesoap")

    def test_can_set_web_group_ownership_on_specified_directory(self):
        """fab.tests.os.akvo_permissions_test  Can set web group ownership on a specified directory"""

        web_dir = "/var/tmp/web/apps"
        self.mock_host_controller.sudo("chown -R root:%s %s" % (AkvoPermissions.WEB_USER_GROUP, web_dir))
        self.mox.ReplayAll()

        self.permissions.set_web_group_ownership_on_directory(web_dir)

    def test_can_set_web_group_permissions_on_specified_directory(self):
        """fab.tests.os.akvo_permissions_test  Can set web group permissions on a specified directory"""

        web_dir = "/var/tmp/web/apps"
        self.mock_host_controller.sudo("chown -R root:%s %s" % (AkvoPermissions.WEB_USER_GROUP, web_dir))
        self.mock_host_controller.sudo("chmod -R g+rw %s" % web_dir)
        self.mock_host_controller.sudo("chmod g+s %s" % web_dir)
        self.mox.ReplayAll()

        self.permissions.set_web_group_permissions_on_directory(web_dir)


def suite():
    return TestSuiteLoader().load_tests_from(AkvoPermissionsTest)

if __name__ == '__main__':
    TestRunner().run_test_suite(suite())
