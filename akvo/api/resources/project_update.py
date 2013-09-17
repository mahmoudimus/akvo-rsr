# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from django.forms.models import ModelForm

from tastypie import fields

from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from akvo.api.authentication import ConditionalApiKeyAuthentication
from akvo.api.fields import Base64FileField, ConditionalFullToOneField
from akvo.api.validation import ModelFormValidation

from akvo.rsr.models import ProjectUpdate

from .resources import ConditionalFullResource


class ProjectUpdateModelForm(ModelForm):
    class Meta:
        model = ProjectUpdate


class ProjectUpdateResource(ConditionalFullResource):
    photo = Base64FileField("photo", blank=True, null=True)
    project = ConditionalFullToOneField('akvo.api.resources.ProjectResource', 'project')
    user = ConditionalFullToOneField('akvo.api.resources.UserResource', 'user')
    organisation = ConditionalFullToOneField(
        'akvo.api.resources.OrganisationResource', attribute='user__userprofile__organisation'
    )

    class Meta:
        allowed_methods         = ['get', 'post']
        authorization           = Authorization()
        authentication          = ConditionalApiKeyAuthentication(methods_requiring_key=['POST'])
        validation              = ModelFormValidation(form_class=ProjectUpdateModelForm)
        queryset                = ProjectUpdate.objects.all()
        resource_name           = 'project_update'
        include_absolute_url    = True
        always_return_data      = True

        filtering               = dict(
            # other fields
            time                = ALL,
            time_last_updated   = ALL,
            title               = ALL,
            update_method       = ALL,
            # foreign keys
            project             = ALL_WITH_RELATIONS,
            user                = ALL_WITH_RELATIONS,
        )

    def dehydrate(self, bundle):
        bundle = super(ProjectUpdateResource, self).dehydrate(bundle)
        bundle.data['full_name'] = "{} {}".format(
            bundle.obj.user.first_name,
            bundle.obj.user.last_name,
        )
        bundle.data['organisation_name'] = bundle.obj.user.get_profile().organisation
        return bundle

    def build_schema(self):
        data = super(ProjectUpdateResource, self).build_schema()
        data['fields']['full_name'] = {
            'default': "No default provided.",
            'type': "string",
            'nullable': False,
            'blank': False,
            'readonly': True,
            'help_text': "The full name of the user posting the update",
            'unique': False,
        }
        data['fields']['organisation_name'] = {
            'default': "No default provided.",
            'type': "string",
            'nullable': False,
            'blank': False,
            'readonly': True,
            'help_text': "The name of organisation of the user posting the update",
            'unique': False,
        }
        return data
