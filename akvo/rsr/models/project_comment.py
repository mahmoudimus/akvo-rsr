# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from akvo.rsr.models import Project


class ProjectComment(models.Model):
    project = models.ForeignKey(Project, verbose_name=_(u'project'), related_name='comments')
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    comment = models.TextField(_(u'comment'))
    time = models.DateTimeField(_(u'time'), db_index=True)

    class Meta:
        verbose_name = _(u'project comment')
        verbose_name_plural = _(u'project comments')
        ordering = ('-id',)
