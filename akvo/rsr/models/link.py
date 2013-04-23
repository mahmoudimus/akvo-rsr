# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from project import Project


class Link(models.Model):
    LINK_KINDS = (
        ('A', _(u'Akvopedia entry')),
        ('E', _(u'External link')),
    )
    kind = models.CharField(_(u'kind'), max_length=1, choices=LINK_KINDS)
    url = models.URLField(_(u'URL'))
    caption = models.CharField(_(u'caption'), max_length=50)
    project = models.ForeignKey(Project, verbose_name=u'project', related_name='links')

    def __unicode__(self):
        return self.url

    def show_link(self):
        return u'<a href="%s">%s</a>' % (self.url, self.caption,)

    class Meta:
        verbose_name = _(u'link')
        verbose_name_plural = _(u'links')

