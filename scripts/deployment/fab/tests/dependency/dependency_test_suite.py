#!/usr/bin/env python

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from testing.helpers.execution import TestRunner, TestSuiteLoader

from fab.tests.dependency.system_package_dependency_test import SystemPackageDependencyTest
from fab.tests.dependency.system_package_dependency_collection_test import SystemPackageDependencyCollectionTest
from fab.tests.dependency.verifier.dependency_verifier_test_suite import dependency_verifier_suite


def dependency_suite():
    dependency_suite = TestSuiteLoader().create_suite_from_classes([SystemPackageDependencyTest, SystemPackageDependencyCollectionTest])

    return TestSuiteLoader().create_suite_from_list([dependency_suite, dependency_verifier_suite()])

if __name__ == '__main__':
    TestRunner().run_test_suite(dependency_suite())
