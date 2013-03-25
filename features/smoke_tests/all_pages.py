# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from lettuce import step, world

@step(u'Visit the page at (\S*)')
def visit_the_page_at(step, url):
    world.browser.visit(url)