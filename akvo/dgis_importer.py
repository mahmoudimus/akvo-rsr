#!/usr/bin/env python
# -*- coding: utf-8 -*-

#to be run in the akvo rsr root folder.


from __future__ import with_statement

import csv
import datetime
import os
import sys
import traceback
import urllib2

from optparse import OptionParser

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.core.files.base import ContentFile
from django.db.models import get_model

from akvo.rsr.models import *

def foo():
    """
    Notes while implemeting the importer
    ====================================
    
    Problems/questions regarding data:
        DGIS is not consitently named:
        Ministry of Foreign Affairs (DGIS) or only DGIS
        The extending org Directie Milieu, Water, Klimaat en Energie has ID NL-1 Is this also DGIS?

        URLs to photos should be just that. Not URLs to web pages with photos or videos.
        
    The Activity location section:
        It is assumed that either all locations are in the same country or that there is
        one location per country. Multiple locs from multiple countries are not supported atm
    

    Org types
        How do we handle org types? Akvo defines 4 types:
            ORG_TYPE_NGO = 'N', _('NGO')
            ORG_TYPE_GOV = 'G', _('Governmental')
            ORG_TYPE_COM = 'C', _('Commercial')
            ORG_TYPE_KNO = 'K', _('Knowledge institution')
        IATI has the following list (based on DAC I think and used by DGIS I presume):
            10	Government
            15	Other Public Sector
            21	International NGO
            22	National NGO
            23	Regional NGO
            30	Public Private Partnership
            40	Multilateral
            60	Foundation
            70	Private Sector
            80	Academic, Training and Research
        How do we reconcile the two? I've made a simple mapping but the larger question is should we
        keep "our" types or migrate to the DAC? And if we migrate how do we handle the current data set?
    """
    pass


SECTIONS = [
    {
        'section': dict( # funding
            first_line='participating org',
            next_line='participating org',
        ),
        'object_info': dict(
            model=u'organisation',
            map={
                'name:': 'name',
                'Org type:': 'organisation_type',
                'ID:': 'iati_id',
                'Role:': 'organisation_partnership'
            }
        )
    },
    {
        'section': dict( # extending
            first_line='participating org',
            next_line='participating org',
        ),
        'object_info': dict(
            model=u'organisation',
            map={
                'name:': 'name',
                'Org type:': 'organisation_type',
                'ID:': 'iati_id',
                'Role:': 'organisation_partnership'
            }
        )
    },
    {
        'section': dict( # implementing
            first_line='participating org',
            next_line='activity location',
        ),
        'object_info': dict(
            model=u'organisation',
            map={
                'name:': 'name',
                'Org type:': 'organisation_type',
                'ID:': 'iati_id',
                'Role:': 'organisation_partnership'
            }
        )
    },
    {
        'section': dict(
            first_line='activity location',
            next_line='websites'
        ),
        'object_info': dict(
            model=u'location',
            map={
                'Country code:': 'country__code',
                'Country name:': 'country',
                'City/village:': 'city',
                'Latitude:': 'latitude',
                'Longitude:': 'longitude',
            }
        )
    },
    {
        'section': dict(
            first_line='websites',
            next_line='photos'
        ),
        'object_info': dict(
            model=u'link',
            map={
                'Description:': 'caption',
                'URL:': 'url',
            }
        )
    },
    {
        'section': dict(
            first_line='photos',
            next_line='activity description'
        ),
        'object_info': dict(
            model=u'image', #special case!
            map={
                'Description:': 'current_image_caption',
                'URL:': 'current_image',
            }
        )
    },
    {
        'section': dict(
            first_line='activity budget and funding',
            next_line='funding'
        ),
        'object_info': dict(
            model=u'budgetitem',
            map={
                'Value:': 'amount',
            }
        )
    },
    {
        'section': dict(
            first_line='funding',
            next_line='indicators'
        ),
        'object_info': dict(
            model=u'fundingpartner',
            map={
                'Value:': 'funding_amount',
                'Provider:': 'funding_organisation',
            }
        )
    },
    {
        'section': dict(
            first_line='indicators',
            next_line='related activities'
        ),
        'object_info': dict(
            model=u'benchmark',
            map={
                'Description:': 'name',
                'Target value:': 'value',
            }
        )
    },
    {
        'section': dict(
            first_line='related activities',
            next_line='extra project information'
        ),
        'object_info': dict(
            model=None, #no implementation yet
            map={
                'Type:': 'activity_type',
                'Identifier:': 'activity_id',
                'Title:': 'title',
            }
        )
    },
]

project_info = dict(
    model=u'project',
    map={
        'Project number:': 'original_id', # NYI - Not Yet Implemented
        'Standard language:': 'default_language', # NYI
        'Standard currency:': 'default_currency', # NYI
        'Title:': 'name',
        'Expected Start date:': 'planned_start_date',
        'Expected End date:': 'planned_end_date',
        'Status code:': 'status',
        'Status text:': '', # Not used
        'Sector code:': 'sector_code', # NYI
        'Sector code text:': '', # Not used
        'IATI Identifier:': 'iati_activity_id', # NYI
        'Organisation ID:': 'iati_org_id', # NYI
        'Other Identifier:': 'original_id', # NYI
        'Collaboration type code': '', # Not used
        'Collaboration type text': '', # Not used
        'Flow type code': '', # Not used
        'Flow type text': '', # Not used
        'Finance type code:': '', # Not used
        'Finance type text:': '', # Not used
        'Identifier': '', # Not used - Akvo is reporting org
        'Type': '', # Not used - Akvo is reporting org
        'Name': '', # Not used - Akvo is reporting org
        'Summary:': 'project_plan_summary',
        'Objectives:': 'goals_overview',
        'Target group:': 'target_group',
        'Output 1:': 'goal_1',
        'Output 2:': 'goal_2',
        'Output 3:': 'goal_3',
        'Output 4:': 'goal_4',
        'Output 5:': 'goal_5',
        'Activity plan details:': 'project_plan_detail',
        'Current status:': 'current_status_detail',
        'Sustainability:': 'sustainability',
        'Local context:': 'context',
    }
)

class RSR_Mapper():
    """data structure that keeps track of all we need to know to create an RSR model
    object from it and set all foreign keys etc we need
    """
    def __init__(self, model=None, fields=None, parent=None):
        self.model  = model
        self.fields = fields or {}
        self.parent = parent
        self.obj    = None

    #def __unicode__(self):
    #    if self.model:
    #        return self.model.__name__ if hasattr(self.model, __name__) else self.model
    #    else:
    #        return 'Model-less mapper'

    def create_organisation(self):
        org_type_mapping = {
            # DAC : Akvo
            '10': Organisation.ORG_TYPE_GOV, # Government : Governmental
            '15': Organisation.ORG_TYPE_GOV, # Other Public Sector : Governmental
            '21': Organisation.ORG_TYPE_NGO, # International NGO : NGO
            '22': Organisation.ORG_TYPE_NGO, # National NGO : NGO
            '23': Organisation.ORG_TYPE_NGO, # Regional NGO : NGO
            '30': Organisation.ORG_TYPE_NGO, # Public Private Partnership : NGO
            '40': Organisation.ORG_TYPE_GOV, # Multilateral : Governmental
            '60': Organisation.ORG_TYPE_NGO, # Foundation : NGO
            '70': Organisation.ORG_TYPE_COM, # Private Sector : Commercial
            '80': Organisation.ORG_TYPE_KNO, # Academic, Training and Research : Knowledge institution
        }
        # lookups
        for k, v in self.fields.iteritems():
            if k == 'organisation_type':
                self.fields[k] = org_type_mapping[v]
        name = self.fields.pop('name')
        self.relations = {'partner_type': self.fields.pop('organisation_partnership')}
        self.obj, created = get_model('rsr',self.model).objects.get_or_create(name=name, defaults=self.fields)
        return self.obj, created

    def link_organisation(self, project):
        if self.relations:
            partner_type = self.relations['partner_type']
            if partner_type == 'Funding':
                obj, created = FundingPartner.objects.get_or_create(project=project, funding_organisation=self.obj, defaults={'funding_amount': 0 })
                self.obj.funding_partner = True
                self.obj.save()
            elif partner_type == 'Extending':
                obj, created = SupportPartner.objects.get_or_create(project=project, support_organisation=self.obj)
                self.obj.support_partner = True
                self.obj.save()
            elif partner_type == 'Implementing':
                obj, created = FieldPartner.objects.get_or_create(project=project, field_organisation=self.obj)
                self.obj.field_partner = True
                self.obj.save()
        return None, None

    def link_fundingpartner(self, project):
        if self.fields.get('funding_amount'):
            org = None
            try:
                org = Organisation.objects.get(name=self.fields['funding_organisation'])
            except:
                try:
                    org = Organisation.objects.get(name='Ministry of Foreign Affairs (DGIS)')
                except:
                    print "Could not find FundingPartner org for %s" % project.__unicode__()
            if org:
                try:
                    funder = FundingPartner.objects.get(project=project, funding_organisation=org)
                    funder.funding_amount = self.fields['funding_amount']
                    funder.save()
                except:
                    print "Could not find FundingPartner obj for %s, %s" % (project.__unicode__(), org.__unicode__())
        return None, None
        
    def link_location(self, project):
        self.fields.pop('country__code') # NYI
        content_type = ContentType.objects.get_for_model(project)
        self.fields.update({'content_type': content_type, 'object_id': project.id, 'primary': project.prime_location})
        project.prime_location = False #only first location is primary
        for k, v in self.fields.iteritems():
            if k == 'country':
                country, new = Country.objects.get_or_create(country_name=self.fields[k], defaults={'continent': 4})
                self.fields[k] = country
                if new:
                    print "Created new country: %s, ID: %d. Please assign a continent the this proud new nation" % (country.country_name, country.id)
        location, created = get_model('rsr',self.model).objects.get_or_create(**self.fields)
        return location, created

    # not used for now. have to fix naming of images and really needs multiple images refactoring in models
    #def link_image(self, project):
    #    import pdb
    #    pdb.set_trace()
    #    try:
    #        contents = urllib2.urlopen(self.fields['current_image']).read()
    #    except urllib2.HTTPError, exc:
    #        # handle exception
    #        pass
    #    file_name = 'foo.jpg'
    #    project.current_image.save(file_name, ContentFile(contents))        

    def link_budgetitem(self, project):
        self.fields.update({'item': 'other', 'project': project}) #we know nuuuthin'bout where the money goes
        self.obj, created = get_model('rsr', self.model).objects.get_or_create(**self.fields)
        return self.obj, created

        
    #class BudgetItem(models.Model):
    #    ITEM_CHOICES = (
    #        ('employment', _('employment')),
    #        ('building', _('building')),
    #        ('training', _('training')),
    #        ('maintenance', _('maintenance')),
    #        ('management', _('management')),
    #        ('other', _('other')),
    #    )
    #    project             = models.ForeignKey(Project)
    #    item                = models.CharField(max_length=20, choices=ITEM_CHOICES, verbose_name=_('Item'))
    #    amount              = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))

    def create_project(self):
        fields_not_yet_implemented = [
            'default_language', # NYI
            'default_currency', # NYI
            'sector_code', # NYI
        ]
        status_mapping = {
            # DAC : Akvo
            '1': 'H', # Pipeline/identification : Needs funding
            '2': 'A', #	Implementation : Active
            '3': 'C', #	Completion : Complete
            '4': 'C', # Post-completion : Complete
            '5': 'L', #	Cancelled : Cancelled
            # Akvo status None has no DAC counterpart
            # Akvo status Archived has no DAC counterpart
        }
        
        # remove fields we're not supporting yet
        for nyi_field in fields_not_yet_implemented:
            self.fields.pop(nyi_field)
        # lookups
        for k, v in self.fields.iteritems():
            if k == 'status':
                self.fields[k] = status_mapping[v]
            if k in ['planned_start_date', 'planned_end_date']:
                try:
                    self.fields[k] = datetime.strptime(self.fields[k], '%d/%b/%y').date()
                except:
                    self.fields[k] = datetime.strptime(self.fields[k], '%d-%b-%y').date()
                    

        
        name = self.fields.pop('name')
                        
        self.obj, created = get_model('rsr', self.model).objects.get_or_create(name=name, defaults=self.fields)
        self.obj.prime_location = True #used in link_location to make first loc primary
        ps = get_model('rsr', 'publishingstatus').objects.get(project=self.obj)
        ps.status = 'published'
        ps.save()
        return self.obj, created

    def link_link(self, project):
        self.fields.update({'kind': 'E', 'project': project}) #assume external link
        self.obj, created = get_model('rsr', self.model).objects.get_or_create(**self.fields)
        return self.obj, created


class CSV_List():
    def __init__(self, data=None, section=None):
        self.data = data or []
        self.section = section or []
    
    def get_rows(self, first_line, next_line=None):
        first = next = -1
        for i in range(len(self.data)):
            if first < 0 and self.data[i][0].strip().lower() == first_line:
                first = i
                if next_line == None:
                    next = first + 1
            elif first > -1 and self.data[i][0].strip().lower() == next_line:
                next = i
            if first  > -1 and next and next > first:
                self.section = self.data[first:next]
                self.data = self.data[:first] + self.data[next:]
                return self.section

    def create_mappings(self, csv_to_oject_map):
        """creates a dict for each set of data that is to be imported as an RSR object
        """
        if csv_to_oject_map.get('model') in ['image', 'fundingpartner']:
            #import pdb
            #pdb.set_trace()
            new_section = {}
            for line in self.section:
                if line[0] in new_section:
                    new_section[line[0]] += line[1:]
                else:
                    new_section[line[0]] = line[1:]
            self.section = [[k]+new_section[k] for k in new_section.iterkeys()]
        max_len = max([len(item) for item in self.section]) - 1 # first item is DGIS "field name"
        mappings = [RSR_Mapper(model=csv_to_oject_map.get('model')) for i in range(max_len)]
        for line in self.section:
            rsr_field = csv_to_oject_map['map'].get(line[0], None)
            if rsr_field:
                for i in range(max_len):
                    try:
                        mappings[i].fields[rsr_field] = line[i+1]
                    except:
                        if len(line) > 1:
                            mappings[i].fields[rsr_field] = line[len(line)-1]
                        else:
                            mappings[i].fields[rsr_field] = ''
        return mappings

def report_on_object(obj, created):
    if created:
        try:
            print "  Created new %s: %s with ID %d." %(obj.__class__.__name__, obj.__unicode__(), obj.id)
        except:
            print "  Bug in report_on_object. Locals: %s" % locals()
    else:
        try:
            print "    Found existing %s: %s with ID %d." %(obj.__class__.__name__, obj.__unicode__(), obj.id)
        except:
            print "    Bug in report_on_object. Locals: %s" % locals()
        
class DGIS_Importer():
    def __init__(self, filename='DGIS_data_short_16635.csv'):
        self.filename = filename
        self.list = CSV_List()
        self.mappings = []
        self.project = None

    def create_objects(self):
        for mapping in self.mappings:
            if mapping.model:
                method = getattr(mapping, "create_%s" % mapping.model, None)
                #try:
                #    method = getattr(mapping, "create_%s" % get_model('rsr', mapping.model).__name__.lower(), False)
                #except:
                if method:
                    obj, created = method()
                    # remember the current Project when we find it
                    if obj.__class__.__name__ == 'Project':
                        self.project = obj
                    report_on_object(obj, created)

        for mapping in self.mappings:
            if mapping.model:
                method = getattr(mapping, "link_%s" % mapping.model, None)
                if method:
                    obj, created = method(self.project)
                    if obj:
                        report_on_object(obj, created)

    def parse_dgis_sheet(self):
        with open(self.filename, 'rtU') as file:
            csv_data = csv.reader(file)
            # create a list of each non-empty row in the csv,
            # each element in the list is one item from the csv
            for row in csv_data:
                row = [item for item in row if item] #remove empty "cells"
                if len(row) > 0:
                    self.list.data.append(row)

            #for item in self.list.data:
            #    print item

            # using SECTIONS, grab a bunch of rows delimited by first_line and next_line
            # that comprise data for one RSR object
            for section in SECTIONS:                
                self.list.get_rows(**section['section'])
                #create a dict with RSR field names (sorta) mapping the grabbed data
                self.mappings.extend(self.list.create_mappings(section['object_info']))

                #print self.mappings
                #print

            # what's left is "raw" project data
            self.list.section = self.list.data
            self.mappings.extend(self.list.create_mappings(project_info))
            self.create_objects()

            #for row in csv_data:
            #    if len(row) > 1:
            #        if data.get(row[0].lower().strip(': '), False):
            #            data[row[0]].extend(row[1:])
            #        else:
            #            data[row[0]] = row[1:]    
            #print unicode(data)


def get_usage():
    usage = """
  %prog [options] action [filelist]:
    action: import
"""
    return usage

def execute_command(argv=None):
    # Use sys.argv if we've not passed in a custom argv
    if argv is None:
        argv = sys.argv

    # Parse the command-line arguments. optparse handles the dirty work.
    parser = OptionParser(usage=get_usage())
    parser.add_option('-d', '--dir', help='Input directory.', default="csv", dest="dir")
    parser.add_option('-v', '--verbose', help='Verbose mode', action='store_true')

    options, args = parser.parse_args(argv[1:])
    
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
        
    options, args = parser.parse_args(argv[1:])
            
    action = args[0]
    apps = args[1:]

    fileExtList = ['.csv']
    directory = options.dir
    fileList = [os.path.normcase(f) for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f) for f in fileList if os.path.splitext(f)[1] in fileExtList]
    for file in fileList:
        try:
            print "Trying to import %s..." % file
            imp = DGIS_Importer(file)
            imp.parse_dgis_sheet()
            print "Success!"
        except:
            print "Failed to import %s." % file
            print traceback.print_exc()
        
if __name__ == '__main__':
    execute_command()
    
    #imp = DGIS_Importer('16635-Table 1.csv')
    #imp.parse_dgis_sheet()
