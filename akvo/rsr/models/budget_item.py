# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from datetime import date, datetime, timedelta
from decimal import Decimal
from textwrap import dedent
from urlparse import urljoin

from django.db import models
from django.utils.translation import ugettext_lazy as _

# from project import Project
from akvo.rsr.utils import RSR_LIMITED_CHANGE


class BudgetItemLabel(models.Model):
    label = models.CharField(_(u'label'), max_length=20, unique=True, db_index=True)

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ('label',)
        verbose_name = _(u'budget item label')
        verbose_name_plural = _(u'budget item labels')


class BudgetItem(models.Model):
    # DON'T translate. Need model translations for this to work
    OTHER_LABELS = [u'other 1', u'other 2', u'other 3']

    project = models.ForeignKey('Project', verbose_name=_(u'project'), related_name='budget_items')
    label = models.ForeignKey(BudgetItemLabel, verbose_name=_(u'label'), )
    other_extra = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_(u'"Other" labels extra info'),
        help_text=_(u'Extra information about the exact nature of an "other" budget item.'),
    )
    # Translators: This is the amount of an budget item in a currency (€ or $)
    amount = models.DecimalField(_(u'amount'), max_digits=10, decimal_places=2, )

    def __unicode__(self):
        return self.label.__unicode__()

    def get_label(self):
        "Needed since we have to have a vanilla __unicode__() method for the admin"
        if self.label.label in self.OTHER_LABELS:
            # display "other" if other_extra is empty. Translating here without translating the other labels seems corny
            return self.other_extra.strip() or u"other"
        else:
            return self.__unicode__()

    class Meta:
        ordering = ('label',)
        verbose_name = _(u'budget item')
        verbose_name_plural = _(u'budget items')
        unique_together = ('project', 'label')
        permissions = (
            ("%s_budget" % RSR_LIMITED_CHANGE, u'RSR limited change budget'),
        )
