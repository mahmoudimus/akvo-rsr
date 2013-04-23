# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from category import Category
from project import Project


class Benchmarkname(models.Model):
    name = models.CharField(_(u'benchmark name'), max_length=50,
                            help_text=_(u'Enter a name for the benchmark. (50 characters).'))
    order = models.IntegerField(_(u'order'), default=0, help_text=_(
        u'Used to order the benchmarks when displayed. Larger numbers sink to the bottom of the list.'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name', ]
        verbose_name = _(u'benchmark name')
        verbose_name_plural = _(u'benchmark names')


class Benchmark(models.Model):
    project = models.ForeignKey(Project, verbose_name=_(u'project'), related_name=_(u'benchmarks'), )
    category = models.ForeignKey(Category, verbose_name=_(u'category'), )
    name = models.ForeignKey(Benchmarkname, verbose_name=_(u'benchmark name'), )
    value = models.IntegerField(_(u'benchmark value'), )

    def __unicode__(self):
        return _(
            u'Category: %(category)s, Benchmark: %(value)d %(name)s'
        ) % {
                   'category': self.category,
                   'value': self.value,
                   'name': self.name,
        }

    class Meta:
        ordering = ('category__name', 'name__order')
        verbose_name = _(u'benchmark')
        verbose_name_plural = _(u'benchmarks')

