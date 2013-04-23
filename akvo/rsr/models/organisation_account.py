# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.db import models

from organisation import Organisation


class OrganisationAccount(models.Model):
    """
    This model keps track of organisation account levels and other relevant data.
    The reason for having this in a separate model form Organisation is to hide
    it from the org admins.
    """
    ACCOUNT_LEVEL = (
        ('free', u'Free'),
        ('plus', u'Plus'),
        ('premium', u'Premium'),
    )
    organisation = models.OneToOneField(Organisation, verbose_name=u'organisation', primary_key=True)
    account_level = models.CharField(u'account level', max_length=12, choices=ACCOUNT_LEVEL, default='free')

    class Meta:
        verbose_name = u'organisation account'
        verbose_name_plural = u'organisation accounts'
