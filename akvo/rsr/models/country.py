# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from akvo.rsr.iso3166 import ISO_3166_COUNTRIES, CONTINENTS


class Country(models.Model):
    name = models.CharField(_(u'country name'), max_length=50, unique=True, db_index=True, )
    iso_code = models.CharField(_(u'ISO 3166 code'), max_length=2, unique=True, db_index=True,
                                choices=ISO_3166_COUNTRIES, )
    continent = models.CharField(_(u'continent name'), max_length=20, db_index=True, )
    continent_code = models.CharField(_(u'continent code'), max_length=2, db_index=True, choices=CONTINENTS)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'country')
        verbose_name_plural = _(u'countries')
        ordering = ['name']

