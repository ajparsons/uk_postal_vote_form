# -*- coding: utf-8 -*-


from django.db import models
from django.db.models import F
from useful_inkleby.useful_django.models import FlexiBulkModel
from tools.ql import QuickList

from useful_inkleby.files import QuickGrid
from oscodepoint import open_codepoint
import datetime
import json

class Election(FlexiBulkModel):
    name = models.CharField(max_length=255, default="", blank=True)
    date = models.DateField()
    cut_off_date = models.DateField(null=True,blank=True)
    
    @classmethod
    def valid_elections(cls):
        n = datetime.datetime.now()
        return list(cls.objects.filter(date__gte=n).order_by('date'))
    
    @classmethod
    def get_time(cls,value):
        universal = False
        single_day = None
        value = int(value)
        time_range = []
        if value == 0:
            universal = True
        elif value == -1:
            range = cls.valid_elections()
            time_range = [range[0].date, range[-1].date]
        else:
            single_day = cls.objects.get(id=value).date
        
        return universal, single_day, time_range
    
    @classmethod
    def populate(cls):
        Election.objects.get_or_create(name="May Elections 2016",
                                       date= datetime.date(2016,05,05))
        Election.objects.get_or_create(name="EU Referendum (June) 2016",
                                       date= datetime.date(2016,06,23))
        Election.objects.get_or_create(name="June General Election 2017",
                                       date= datetime.date(2017,6,8))     
        

class Council(FlexiBulkModel):
    name = models.CharField(max_length=255, default="", blank=True)
    website = models.CharField(max_length=255, default="", blank=True)
    postcode = models.CharField(max_length=9, default="", blank=True)
    lad13cd = models.CharField(max_length=13, default="", blank=True)
    address = models.TextField(default=00)
    email = models.CharField(max_length=255, default="", blank=True)
    phone = models.CharField(max_length=255, default="", blank=True)
    forms_completed = models.IntegerField(default=0)
    

    @classmethod
    def from_postcode(cls,postcode):
        """
        given a postcode - try and get the local council
        """
        def reduce(txt):
            return txt.lower().strip().replace(" ", "")
        
        r_postcode = reduce(postcode)
        
        try:
            return Postcode.objects.get(postcode=r_postcode).council
        except Postcode.DoesNotExist:
            return None
            
    def increment_count(self):
        self.forms_completed = F('forms_completed') +1
        self.save()
                
    
    @classmethod
    def populate(cls):
        """
        populate councils with ERO contact details
        source : 
        
        """

        with open('..//resources//councils.json') as data_file:    
            data = json.load(data_file)
        Council.objects.all().delete()
        for r in data:
            Council(name=r["name"],
                    website = r["website"],
                    postcode = r["postcode"],
                    email=r["email"],
                    lad13cd = r["council_id"],
                    phone = r["phone"],
                    address = r["address"]
                    ).queue()
            
        Council.save_queue()
        
    

class Postcode(FlexiBulkModel):
    """
    stores reduced vesion of OS code point
     open for council and postcode connection
    """
    postcode = models.CharField(
        max_length=7, blank=True, db_index=True)  # lower and spaces removed
    council = models.ForeignKey(
        Council, null=True, blank=True, related_name="postcode_refs")
    multi_council = models.IntegerField(default=0)

    @classmethod
    def is_multi(cls,postcode):
        """
        given a postcode - try and get the local council
        """
        def reduce(txt):
            return txt.lower().strip().replace(" ", "")
        
        r_postcode = reduce(postcode)
        
        try:
            return Postcode.objects.get(postcode=r_postcode).multi_council
        except Postcode.DoesNotExist:
            return None

    @classmethod
    def populate(cls,delete_current=False):
        """ load postcodes through oscodepoint interfaces"""
        if delete_current:
            print "deleted {0}".format(cls.objects.all().delete())
        
        def reduce(txt):
            return txt.lower().strip().replace(" ", "")
        
        codepoint = open_codepoint('..//resources//codepo_gb.zip')
        split = QuickGrid().open('..//resources/split-postcodes.csv')
        
        split_lookup = {reduce(x["postcode"]):int(x["authorities"]) for x in split}
        
    
        Postcode.objects.all().delete()
    

    
        total = codepoint.metadata['total_count']
        print "{0} total".format(total)
    
        council_lookup = {x.lad13cd: x.id for x in Council.objects.all()}
    
        for x, entry in enumerate(codepoint.entries()):
    
            try:
                council = council_lookup[entry['Admin_district_code']]
            except KeyError:
                council = None
                print "{0} doesn't exist in our councils".format(entry['Admin_district_code'])
    
            code = reduce(entry['Postcode'])
            multi = split_lookup.get(code,1)
            Postcode(postcode=code,
                     council_id=council,
                     multi_council=multi).queue()
                     
        Postcode.save_queue(5000)
                     

