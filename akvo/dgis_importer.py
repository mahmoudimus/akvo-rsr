#!/usr/bin/env python
# -*- coding: utf-8 -*-

#to be run in the akvo rsr root folder.


from __future__ import with_statement

from django.core.management import setup_environ
import settings
setup_environ(settings)

from os.path import basename, splitext
import csv
import datetime

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
            model=Organisation,
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
            model=Organisation,
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
            model=Organisation,
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
            model=Location,
            map={
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
            model=Link,
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
            model=None,
            map={
                'Description:': 'current_image_caption',
                'URL:': 'current_image',
            }
        )
    },
    {
        'section': dict(
            first_line='funding',
            next_line='indicators'
        ),
        'object_info': dict(
            model=FundingPartner,
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
            model=Benchmark,
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
            model=Link,
            map={
                'Type:': 'activity_type',
                'Identifier:': 'activity_id',
                'Title:': 'title',
            }
        )
    },
]

project_info = dict(
    model=Project,
    map={
        'Project number:': 'original_id', # NYI - Not Yet Implemented
        'Standard language:': 'default_language', # NYI
        'Standard currency:': 'default_currency', # NYI
        'Title:': 'name',
        'Expected Start date:': 'planned_start_date', # NYI
        'Expected End date:': 'planned_end_date', # NYI
        'Status code:': 'status',
        'Status text:': '', # Not used
        'Sector code:': 'sector_code', # NYI
        'Sector code text:': '', # Not used
        'IATI Identifier:': 'iati_activity_id', # NYI
        'Organisation ID:': 'other_iati_org_id', # NYI
        'Other Identifier:': 'other_original_id', # NYI
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
        'Target group:': 'target_group', # NYI
        'Output 1:': 'goal_1',
        'Output 2:': 'goal_2',
        'Output 3:': 'goal_3',
        'Output 4:': 'goal_4',
        'Output 5:': 'goal_5',
        'Value:': 'budgetitem_set',
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
        
        self.obj, created = self.model.objects.get_or_create(name=name, defaults=self.fields)
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
            print obj, created

    def create_project(self):
        fields_not_yet_implemented = [
            'original_id', # NYI - Not Yet Implemented
            'default_language', # NYI
            'default_currency', # NYI
            #'planned_start_date', # NYI
            #'planned_end_date', # NYI
            'sector_code', # NYI
            'iati_activity_id', # NYI
            'other_iati_org_id', # NYI
            'other_original_id', # NYI
            #'target_group', # NYI
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
                self.fields[k] = datetime.strptime(self.fields[k], '%d/%b/%y').date()

        
        name = self.fields.pop('name')
        budgetitem_set = self.fields.pop('budgetitem_set')
                
        self.obj, created = self.model.objects.get_or_create(name=name, defaults=self.fields)
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
        """creates a dics for each set of data that is to be iported as an RSR object
        """
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

class DGIS_Importer():
    def __init__(self, filename='DGIS_data_short_16635.csv'):
        self.filename = filename
        self.list = CSV_List()
        self.mappings = []
        self.project = None

    def create_objects(self):
        for mapping in self.mappings:
            if mapping.model:
                method = getattr(mapping, "create_%s" % mapping.model.__name__.lower(), False)
                if method:
                    obj, created = method()
                    # remember the current Project when we find it
                    if obj.__class__.__name__ == 'Project':
                        self.project = obj
        for mapping in self.mappings:
            if mapping.model:
                method = getattr(mapping, "link_%s" % mapping.model.__name__.lower(), False)
                if method:
                    method(self.project)

    def parse_dgis_sheet(self):
        with open(self.filename, 'r') as file:
            csv_data = csv.reader(file)
            # create a list of each non-empty row in the csv,
            # each element in the list is one item from the csv
            for row in csv_data:
                row = [item for item in row if item] #remove empty "cells"
                if len(row) > 0:
                    self.list.data.append(row)

            for item in self.list.data:
                print item

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


if __name__ == '__main__':
    #while test_data:
    #    try:
    #        test_data, extracted = get_rows(test_data[0][0], test_data[1][0], test_data)
    #        print test_data
    #        print extracted
    #    except IndexError:
    #        pass
    imp = DGIS_Importer('16635-Table 1.csv')
    imp.parse_dgis_sheet()
