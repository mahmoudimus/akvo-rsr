# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from textwrap import dedent

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from akvo.rsr.fields import NullCharField

from organisation import Organisation


class PartnerSite(models.Model):
    def about_image_path(instance, file_name):
        return 'db/partner_sites/%s/image/%s' % (instance.hostname, file_name)

    def custom_css_path(instance, filename):
        return 'db/partner_sites/%s/custom.css' % instance.hostname

    def custom_favicon_path(instance, filename):
        return 'db/partner_sites/%s/favicon.ico' % instance.hostname

    def custom_logo_path(instance, filename):
        return 'db/partner_sites/%s/logo/%s' % (instance.hostname, filename)

    organisation = models.ForeignKey(Organisation, verbose_name=_(u'organisation'),
                                     help_text=_('Select your organisation from the drop-down list.')
    )
    hostname = models.CharField(_(u'hostname'), max_length=50, unique=True,
                                help_text=_(
                                    u'<p>Your hostname is used in the default web address of your partner site. '
                                    u'The web address created from  the hostname <em>myorganisation</em> would be '
                                    u'<em>http://myorganisation.akvoapp.org/</em>.</p>'
                                )
    )
    cname = NullCharField(_(u'CNAME'), max_length=100, unique=True, blank=True, null=True,
                          help_text=_(
                              u'<p>Enter a custom domain name for accessing the partner site, '
                              u'for example <i>projects.mydomain.org</i>. Optional. Requires additional DNS setup.</p>'
                          )
    )
    custom_return_url = models.URLField(_(u'Return URL'), blank=True,
                                        help_text=_(
                                            u'<p>Enter the full URL (including http://) for the page to which users '
                                            u'should be returned when leaving the partner site.</p>'
                                        )
    )
    custom_css = models.FileField(_(u'stylesheet'), blank=True, upload_to=custom_css_path)
    custom_logo = models.FileField(_(u'organisation banner logo'), blank=True, upload_to=custom_logo_path,
                                   help_text=_(
                                       u'<p>Upload a logo file for the banner at the top of the partner site page. '
                                       u'By default the logo currently used by www.akvo.org will be displayed.</p>'
                                   )
    )
    custom_favicon = models.FileField(_(u'favicon'), blank=True, upload_to=custom_favicon_path,
                                      help_text=_(
                                          u"<p>A favicon (.ico file) is the 16x16 pixel image shown inside the browser's location bar, "
                                          u'on tabs and in the bookmark menu.</p>'
                                      )
    )
    about_box = models.TextField(_(u'about box text'), max_length=500, blank=True,
                                 help_text=_(dedent(u'''
            Enter HTML that will make up the top left box of the home page. (500 characters)
            <p>
                Any text added should be wrapped in 2 &lt;div&gt; tags, an outer one specifying position and width
                of the text, and an inner for formatting of the text .
            </p>
            <p>
                The Outer &lt;div&gt; tag can use the classes <code>quarter, half, three_quarters and full</code> to
                specify the
                width of the text. It can use the classes <code>bottom</code> and <code>right</code> to specify a position other than top left.
            </p>
            <p>
                The Inner &lt;div&gt; tag can use the class <code>text_bg</code> to create a semi-transparent text
                background if a background image will be uploaded. Any other inline styles can also be used within the
                inner &lt;div&gt;. The tags &lt;h1&gt;, &lt;h3&gt;, &lt;h5&gt; and &lt;a&gt; are blue, while &lt;p&gt;
                tags are black by default. Use the classes <code>first</code> and <code>last</code> with &lt;p&gt; tags
                to reduce the margins above or below respectively.
            </p>
            <p>
                Add additional styling inline, or upload a .css stylesheet in the Stylesheet setting above.
                <em>Tip:</em> When using a .css file, use the #about_box ID selector to apply a style only to
                the About box.
            </p>
        '''))
    )
    about_image = models.ImageField(_(u'about box image'), blank=True, upload_to=about_image_path,
                                    help_text=_(u'''<p>The optional background image for the About box
            <em>must</em> be 470 pixels wide and 250 pixels tall.</p>
        ''')
    )

    enabled = models.BooleanField(_(u'enabled'), default=True)
    default_language = models.CharField(_(u'Site UI default language'),
                                        max_length=5,
                                        choices=settings.LANGUAGES,
                                        default=settings.LANGUAGE_CODE)

    ui_translation = models.BooleanField(_(u'Translate user interface'), default=False)
    google_translation = models.BooleanField(_(u'Google translation widget'), default=False)

    def __unicode__(self):
        return u'Partner site for %(organisation_name)s' % {'organisation_name': self.organisation.name}

    @property
    def logo(self):
        return self.custom_logo or None

    @property
    def return_url(self):
        return self.custom_return_url or self.organisation.url

    @property
    def stylesheet(self):
        return self.custom_css or None

    @property
    def favicon(self):
        return self.custom_favicon or None

    @property
    def full_domain(self):
        return '%s.%s' % (self.hostname, settings.APP_DOMAIN_NAME)

    def get_absolute_url(self):
        url = ''
        # TODO: consider the ramifications of get_absolute_url using CNAME if available
        if self.cname:
            return self.cname

        protocol = 'http'
        if getattr(settings, 'HTTPS_SUPPORT', True):
            protocol = '%ss' % protocol

        url = '%s://%s/' % (protocol, self.full_domain)
        return url

    class Meta:
        verbose_name = u'partner site'
        verbose_name_plural = u'partner sites'
        ordering = ('organisation__name',)