# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module. 
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode

from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer, get_type_string

import inspect

from lxml import etree
from lxml.builder import ElementMaker #, E

from akvo.rsr.models import Project, Category, Link, FundingPartner, SupportPartner, Organisation

#.GenericRelation(Location)

def who_is_parent():
    """
    introspecting function returning the name of the caller of the function
    where who_is_parent is called
    """
    return inspect.stack()[2][3]

XML_NS      = "http://www.w3.org/XML/1998/namespace"
AKVO_NS     = "http://www.akvo.org/rsr/api"
NS_MAP = {
    "xml":   XML_NS,
    "akvo":  AKVO_NS,
}        
A = ElementMaker(nsmap=NS_MAP, namespace=AKVO_NS)
E = ElementMaker(nsmap=NS_MAP)

class EDNA(object):
    """Element Data'N'Attributes
    """
    def __init__(self, name, data, attrib=None):
        self.name = name
        self.data = data
        self.attrib = attrib or {}

    def __repr__(self):
        return "<EDNA - tag: %s data: %s attrs: %s>" % (self.name, str(self.data), str(self.attrib))

class ParentedElement(object):
    def __init__(self, bundle, element, parent):
        self.bundle = bundle
        self.element = element
        self.parent = parent
    
    def set_in_tree(self):
        if self.parent:
            parent = self.bundle.data[self.parent]
            if isinstance(parent, ParentedElement):
                parent.element.append(self.element)
            else:
                parent.append(self.element)
                
    
class IATISerializer(Serializer):
    formats = ['xml',]
    content_types = {
        'xml': 'application/xml',
    }
    
    #def to_xml(self, data, options=None):
    #    #import pdb
    #    #pdb.set_trace()
    #    options = options or {}
    #    XML_NS      = "http://www.w3.org/XML/1998/namespace"
    #    AKVO_NS     = "http://www.akvo.org/rsr/api"
    #    NS_MAP = {
    #        "xml":   XML_NS,
    #        "akvo":  AKVO_NS,
    #    }
    #    #akvo namspaced element
    #    tree = self.to_etree(data, options)
    #    import pdb
    #    pdb.set_trace()
    #    
    #    A = ElementMaker(nsmap=NS_MAP, namespace=AKVO_NS)
    #
    #    import pdb
    #    pdb.set_trace()
    #    if isinstance(data, dict):
    #        return self.to_xml(data['objects'], options)
    #    if isinstance(data, (tuple, list)):
    #        for item in data:
    #            return self.to_xml(item, options)
    #    elif isinstance(data, Bundle):
    
    #def to_xml(self, data, options=None):
    #    options = options or {}
    #    XML_NS      = "http://www.w3.org/XML/1998/namespace"
    #    AKVO_NS     = "http://www.akvo.org/rsr/api"
    #    NS_MAP = {
    #        "xml":   XML_NS,
    #        "akvo":  AKVO_NS,
    #    }
    #    #akvo namspaced element
    #    A = ElementMaker(nsmap=NS_MAP, namespace=AKVO_NS)
    #    page = E(
    #        'iati-activites',
    #        E(
    #            'iati-activity',
    #            E(
    #                'iati-identifier',
    #                'Akvo-%d' % data.obj.pk
    #            ),
    #            A(
    #                'project-summary',
    #                data.obj.project_plan_summary,
    #            ),
    #            {
    #                '{%s}lang' % XML_NS: 'eng',
    #                'default-currency': 'EUR',
    #                'hierarchy': '1',
    #                'last-updated': u'Now!'
    #            },
    #        ),
    #        E(
    #            'iati-activity',
    #            {'{%s}lang' % XML_NS: 'eng'}
    #        ),
    #        {'generated-datetime':u'Närdå?'}, version='1.00'
    #    )
    #    return etree.tostring(page, pretty_print=True, xml_declaration=True, encoding='utf-8')

    def to_etree(self, data, options=None, name=None, depth=0):
        """
        Given some data, converts that data to an ``etree.Element`` suitable
        for use in the XML output.
        
        Bundle(
            data = {'data':
                EDNA('iati-activity'
                    [
                        {'iati-identifier': 'Akvo-%s' % Project.pk},
                        EDNA('reporting-org', 'Akvo foundation', dict(ref="AKVO")),
                        EDNA('description', Project.project_plan_summary, dict(type="General")),
                        EDNA('description', Project.project_plan_detail, {'{%s}type' % AKVO_NS: 'Current status'}),
                        EDNA('description', Project.sustainability, {'{%s}type' % AKVO_NS: 'Sustainability'),
                        EDNA('description', Project.context, {'{%s}type' % AKVO_NS: 'Context'}),
                        EDNA('description', Project.goals_overview, dict(type="Objectives")),
                    ], {
                        '{%s}lang' % XML_NS: 'en', default-currency="EUR" hierarchy="1" last-updated-datetime"2001-01-01"
                    }
                )
            }
        )
        
        """
        if isinstance(data, Bundle):
            element = E(name or 'iati-activities')
            element.append(self.to_etree(data.data['tasty_data'], options, depth=depth+1))
            return element
        elif isinstance(data, EDNA):
            element = E(data.name or 'object', data.attrib)
            if isinstance(data.data, (list, tuple)):
                for item in data.data:
                    element.append(self.to_etree(item, options, depth=depth+1))
            else:
                simple_data = self.to_simple(data.data, options)
                data_type = get_type_string(simple_data)
                if data_type != 'null':
                    element.text = force_unicode(simple_data)                
            return element
        
        else:
            return super(IATISerializer, self).to_etree(data, options, name, depth)


class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'


class ProjectResource(ModelResource):
    categories = fields.ToManyField(CategoryResource, 'categories')
    links = fields.ToManyField('akvo.rsr.api.resources.LinkResource', 'links')
    fundingpartners = fields.ToManyField('akvo.rsr.api.resources.FundingPartnerResource', 'fundingpartner_set', full=True)
    
    class Meta:
        queryset = Project.objects.active()
        resource_name = 'project'

class IATIActivityResource(ModelResource):
    """
    We wanna create XML looking like this:
    
    <iati-acitvity xml:lang="en" default-currency="EUR" hierarchy="1" last-updated-datetime"2001-01-01">
      <iati-identifier>Akvo-{{Project.id}}</iati-identifier>
      <reporting-org ref='AKVO'>Akvo foundation</reporting-org>
      <!-- describing text fields -->
      <description type="General">Project.project_plan_summary</description>
      <description akvo:type="Details">Project.project_plan_detail</description>
      <description akvo:type="Current status">Project.current_status_detail</description>
      <description akvo:type="Sustainability">Project.sustainability</description>
      <description akvo:type="Context">Project.context</description>
      <description type="Objectives">Project.goals_overview</description>
      <participating-org role="Extending" type="Government" ref="NL-1">DGIS</participating-org>
      <title>Water supply for Nyanje school in Zambia</title>
      <other-identifier owner-ref="GB-1" owner-name="DFID">105838-1</other-identifier>
    </iati-acitvity>

    We construct the following data structure:
    
    Bundle(
        data = {'tasty_data':
            EDNA('iati-activity',
                [
                    EDNA('iati-identifier', 'Akvo-%s' % Project.pk),
                    EDNA('reporting-org', 'Akvo foundation', dict(ref="AKVO")),
                    EDNA('description', Project.project_plan_summary, dict(type="General")),
                    EDNA('description', Project.project_plan_detail, {'{%s}type' % AKVO_NS: 'Current status'}),
                    EDNA('description', Project.sustainability, {'{%s}type' % AKVO_NS: 'Sustainability'),
                    EDNA('description', Project.context, {'{%s}type' % AKVO_NS: 'Context'}),
                    EDNA('description', Project.goals_overview, dict(type="Objectives")),
                    EDNA('title', Project.name),
                    EDNA('other-identifier', Project.orig_id, {'owner-ref': 'NL-1', 'owner-name': 'DGIS'}),
                    
                    EDNA('participating-org', Project.NNNpartner.NNN_organisation.name, dict(role="NNNpartner", type="Organisation.type", ref="Organisation.iati_id")),
                ], {
                    '{%s}lang' % XML_NS: 'en', default-currency="EUR" hierarchy="1" last-updated-datetime"2001-01-01"
                }
                )
            }
        }
    )
        
    """
    categories = fields.ToManyField(CategoryResource, 'categories')
    links = fields.ToManyField('akvo.rsr.api.resources.LinkResource', 'links')
    fundingpartners = fields.ToManyField('akvo.rsr.api.resources.FundingPartnerResource', 'fundingpartner_set', full=True)
    

    class Meta:
        queryset = Project.objects.active()
        resource_name = 'iati-activity'
        serializer = IATISerializer()
    
    def bundler(self, bundle, tag_name, attrib=None, parent=None):
        """create an lxml Element and assign it to the bundle.data
        get the field name by removing "dehydrate_" from who_is_parent
        use the field name to get the original data from the bundle
        create the Element using the tag_name, the original data and any supplied attributes
        remove field_name data from bundle.data
        """
        field_name = '_'.join(who_is_parent().split('_')[1:])
        attrib = attrib or {}
        data = bundle.data
        if data[field_name]:
            result = EDNA(tag_name, data[field_name], attrib)
            
            if parent:
                if isinstance(data['tasty_data'],  EDNA):
                    data['tasty_data'].data.append(result)
                else:
                    data['tasty_data'].data = [result]
            else:
                data['tasty_data'] = result
        data.pop(field_name)
        
    def dehydrate_id(self, bundle):
        id = bundle.data['id']
        bundle.data['id'] = 'Akvo-%s' % id
        self.bundler(bundle, 'iati-identifier', {'ref': id}, 'iati-activity')
        bundle.data['id'] = "http://%s%s" % (Site.objects.get_current(), reverse('project_main', args=[id]))
        self.bundler(bundle, 'activity-website', {}, 'iati-activity')
        
    def dehydrate_project_plan_summary(self, bundle):
        self.bundler(bundle, 'description', {'type': 'General'}, 'iati-activity')
    
    def dehydrate_project_plan_detail(self, bundle):
        self.bundler(bundle, 'description', {'{%s}type' % AKVO_NS: 'Details'}, 'iati-activity')
    
    def dehydrate_current_status_detail(self, bundle):
        self.bundler(bundle, 'description', {'{%s}type' % AKVO_NS: 'Current status'}, 'iati-activity')

    def dehydrate_sustainability(self, bundle):
        self.bundler(bundle, 'description', {'{%s}type' % AKVO_NS: 'Sustainability'}, 'iati-activity')

    def dehydrate_goals_overview(self, bundle):
        self.bundler(bundle, 'description', {'type': 'Objectives'}, 'iati-activity')

    def dehydrate_name(self, bundle):
        self.bundler(bundle, 'title', {}, 'iati-activity')

    def dehydrate_original_id(self, bundle):
        self.bundler(bundle, 'other-identifier', {'owner-ref': 'NL-1', 'owner-name': 'DGIS'}, 'iati-activity')

    def dehydrate_fundingpartners(self, bundle):
        def dehydrate_fundingpartner(*args):
            self.bundler(*args)

        for item in bundle.data['fundingpartners']:
            bundle.data['fundingpartner'] = item.data['funding_organisation'].data['name']
            dehydrate_fundingpartner(bundle, 'participating-org', {'role': item.data['funding_organisation'].data['role']}, 'iati-activity')

    def dehydrate_supportpartners(self, bundle):
        def dehydrate_supportpartner(*args):
            self.bundler(*args)

        for item in bundle.data['supportpartners']:
            bundle.data['supportpartner'] = item.data['support_organisation'].data['name']
            dehydrate_supportpartner(bundle, 'participating-org', {'role': item.data['support_organisation'].data['role']}, 'iati-activity')

    def full_dehydrate(self, obj):
        """
        Given an object instance, extract the information from it to populate
        the resource.
        
        Override of Resource.full_dehydrate()
        """
        bundle = Bundle(obj=obj)
        # create root node of an iati-activity
        bundle.data = {'tasty_data':
            EDNA('iati-activity',[
                    EDNA('reporting-org', 'Akvo foundation', dict(ref="AKVO", type="60"))
                ], {
                'hierarchy': '1',
                'default-currency': 'EUR',
                '{http://www.w3.org/XML/1998/namespace}lang': 'en',
                'last-updated-datetime': '2011-05-10'
            })
        }
        # Dehydrate each field.
        for field_name, field_object in self.fields.items():
            print field_name, field_object
            # A touch leaky but it makes URI resolution work.
            if isinstance(field_object, fields.RelatedField):
                field_object.api_name = self._meta.api_name
                field_object.resource_name = self._meta.resource_name
                bundle.data[field_name] = field_object.dehydrate(bundle)
                
            
            # Check for an optional method to do further dehydration.
            meth_name = "dehydrate_%s" % field_name
            method = getattr(self, meth_name, None)
            
            if method:
                if meth_name == 'dehydrate_resource_uri':
                    bundle.data[field_name] = method(bundle)
                else:
                    bundle.data[field_name] = field_object.dehydrate(bundle)
                    method(bundle)
        
        bundle = self.dehydrate(bundle)
        #import pdb
        #pdb.set_trace()
        return bundle


class LinkResource(ModelResource):
    project = fields.ToOneField(ProjectResource, 'project')
    
    class Meta:
        queryset = Link.objects.all()
        resource_name = 'links'

class OrganisationResource(ModelResource):
    #fundingpartners = fields.ToManyField('akvo.rsr.api.resources.FundingPartnerResource', 'funding_partners')
    
    class Meta:
        queryset = Organisation.objects.all()
        
class FundingPartnerResource(ModelResource):
    project = fields.ToOneField(ProjectResource, 'project')
    funding_organisation = fields.ToOneField(OrganisationResource, 'funding_organisation', full=True)

    def dehydrate_funding_organisation(self, bundle):
        data = {'name': bundle.data['funding_organisation'].data['name'], 'role': 'Funding'}
        return Bundle(data=data)
        
    class Meta:
        queryset = FundingPartner.objects.all()
        resource_name = 'fundingpartners'

        
class SupportPartnerResource(ModelResource):
    project = fields.ToOneField(ProjectResource, 'project')
    support_organisation = fields.ToOneField(OrganisationResource, 'support_organisation', full=True)

    def dehydrate_support_organisation(self, bundle):
        data = {'name': bundle.data['support_organisation'].data['name'], 'role': 'Extending'}
        return Bundle(data=data)
        
    class Meta:
        queryset = SupportPartner.objects.all()
        resource_name = 'supportpartners'
