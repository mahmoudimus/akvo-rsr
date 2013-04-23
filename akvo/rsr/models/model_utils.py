# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

#Custom manager
#based on http://www.djangosnippets.org/snippets/562/ and
#http://simonwillison.net/2008/May/1/orm/

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


OLD_CONTINENTS = (
    ("1", _(u'Africa')),
    ("2", _(u'Asia')),
    ("3", _(u'Australia')),
    ("4", _(u'Europe')),
    ("5", _(u'North America')),
    ("6", _(u'South America')),
)

CURRENCY_CHOICES = (
    ('USD', '$'),
    ('EUR', '€'),
)

STATUSES = (
    ('N', _(u'None')),
    ('H', _(u'Needs funding')),
    ('A', _(u'Active')),
    ('C', _(u'Complete')),
    ('L', _(u'Cancelled')),
    ('R', _(u'Archived')),
)
STATUSES_COLORS = {'N': 'black', 'A': '#AFF167', 'H': 'orange', 'C': 'grey', 'R': 'grey', 'L': 'red', }


UPDATE_METHODS = (
    ('W', _(u'web')),
    ('E', _(u'e-mail')),
    ('S', _(u'SMS')),
)
