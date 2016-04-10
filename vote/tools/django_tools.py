# -*- coding: utf-8 -*
'''
Helpful django things

will be tidied up into it's own project at some point

'''

from django.db import models
from django.utils import timezone
from django.shortcuts import render, render_to_response, RequestContext
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.core.handlers.base import BaseHandler  
from django.test.client import RequestFactory 
from django.http import HttpResponse
from django.conf import settings
import codecs
import os
from markdown import markdown
from htmlmin.minify import html_minify
import io




class RequestMock(RequestFactory):  
    def request(self, **request):
        #https://gist.github.com/tschellenbach/925270
        "Construct a generic request object."  
        request = RequestFactory.request(self, **request)  
        handler = BaseHandler()  
        handler.load_middleware()  
        for middleware_method in handler._request_middleware:  
            if middleware_method(request):  
                raise Exception("Couldn't create request mock object - "  
                                "request middleware returned a response")  
        return request 


def use_template(template):
    """
    decorator for making functions look nicer
    """
    def outer(func):  
        def inner(request,*args,**kwargs):
            return render_to_response(template,
                                      context=func(request,*args,**kwargs),
                                      context_instance=RequestContext(request))
        return inner
    return outer


class MarkDownView(object):
    """
    allows for a basic view where a markdown file is read in and rendered
    """
    markdown_loc = ""
    
    def get_markdown(self):
        f = codecs.open(self.__class__.markdown_loc, "rb", "cp1252")
        txt = f.read()
        md = mark_safe(markdown(txt))
        return md
    
    def view(self,request):
        return {"markdown":self.get_markdown()}
        

class BakeView(object):
    """
    
    BakeView - class preserving functional view logic while hiding more configuration in the
    classes. 
    
    Allows for static site generation. 
    
    classes should have a view function that expects self, request. 
    
    url configurations are kept in this class - see local method for how to hook this up
    to the view
    
    """
    
    template = ""
    url_pattern = ""
    url_patterns = []
    url_pattern_name = ""
    bake_path = ""
    
    @classmethod
    def get_pattern(cls):
        """
        returns a list of conf.url objects for url patterns that match this object
        """
        new_patterns = []
        def urlformat(pattern):
            return url(pattern,cls.as_view(),name=cls.url_pattern_name)
        
        if cls.url_patterns:
            new_patterns = [urlformat(x) for x in cls.url_patterns]
        if cls.url_pattern:
            new_patterns.append(urlformat(cls.url_pattern))
            
        return new_patterns
    @classmethod
    def local(cls):
        """
        returns a local subclass of BakeView that lets you access all views in one app at
        the same time - to connect to patterns.
        
        so in view:
        
        LocalBake = BakeView.local()
        
        then all views are subclasses of this
        
        to set up urls
        
        in a urls.py - import views.LocalBake
        
        then urlpatterns += LocalBake.patterns()
        
        
        """
        class LocalBake(cls):
            
        
            
            @classmethod
            def patterns(lb):
                local_patterns = []
                for c in lb.get_subclasses():
                    local_patterns.extend(c.get_pattern())
                    
                local_patterns.sort(key = lambda x:len(x._regex), reverse=True)
                return local_patterns

        
        return LocalBake

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            for c in subclass.get_subclasses():
                yield c
            yield subclass
    

    @classmethod
    def as_view(cls):
        """
        inner func hides that we need to pass a self arg to the view
        """
        
        def render_func(request,*args,**kwargs):
            context = cls().view(request,*args,**kwargs)
            if isinstance(context,HttpResponse):
                return context
            else:
                return cls().context_to_html(request,context)
            
        return render_func

    def context_to_html(self,request,context):
        html = render(request,
                      self.__class__.template,
                      context=context,
                      context_instance=RequestContext(request)
                      )
        return html

    @classmethod
    def bake_children(cls, **kwargs):
        for c in cls.get_subclasses():
            if c.bake_path:
                c.bake(**kwargs)

    @classmethod
    def bake(cls,limit_query=None,**kwargs):
        """
        render all versions of this view into a file
        """
        if cls.bake_path:
            print "baking {0}".format(cls.__name__)
            i = cls()
            for o in i.bake_args(limit_query):
                if o == None:
                    i.render_to_file(**kwargs)
                else:
                    i.render_to_file(o,**kwargs)
        else:
            raise ValueError("This view has no location to bake to.")
    
    def render_to_file(self,args=None,only_absent=False):
        """
        renders this set of arguments to a file
        """
        if args == None:
            file_path = os.path.join(settings.BAKE_LOCATION,
                                     self.__class__.bake_path)
            args = []
        else:
            file_path = os.path.join(settings.BAKE_LOCATION,
                                     self.__class__.bake_path.format(*args))
        
        if only_absent and os.path.isfile(file_path):
            return None
        
        print "saving {0}".format(file_path)
        directory = os.path.dirname(file_path)
        if os.path.isdir(directory) == False:
            os.makedirs(directory)
        
        request = RequestMock().request()
        
        request.path = "/" + file_path.replace(settings.BAKE_LOCATION,"").replace("\\","/").replace("index.html","").replace(".html","")

        context = self.view(request,*args)
        html = html_minify(self.context_to_html(request,context).content)
        
        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        


    def bake_args(self):
        """
        subclass with a generator that feeds all possible arguments into the view
        """
        return [None]

    def view(self,request):
        """
        dummy view- should almost always be subclassed out (unless raw template)
        """
        return {}
    
  
    


class StockModelHelpers(object):
    """
    common functions useful for all models - diagnostics etc
    """
    def __unicode__(self):
        if hasattr(self,"name"):
            return self.name
        else:
            return unicode(self.id)

class EasyBulkModel(models.Model):
    """
    streamlines bulk creation - adds queue to inv objects and do_queue to the class - that forces it to exist.
    """
    batch_time = models.DateTimeField(null=True,blank=True, editable=False)
    batch_id = models.IntegerField(null=True,blank=True, editable=False)
    __queue = []
    
    class Meta:
        abstract = True

    @classmethod
    def add_to_queue(cls,obj):
        cls.__queue.append(obj)
        
    @classmethod  
    def do_queue(cls,safe_creation_rate = 1000, retrieve=True):
        """
        adds references to objects so they can be retrieved in 
        simplist possible query and values attached to existing objects
        """
        n = timezone.now()
        
        for x, q in enumerate(cls.__queue):
            q.batch_id = x
            q.batch_time = n
        
        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in xrange(0, len(l), n):
                yield l[i:i+n]
        
        for c in chunks(cls.__queue,safe_creation_rate):
            print "saving {0} of {1}".format(len(c),cls)
            cls.objects.bulk_create(c)
        
        returning = []
        if retrieve:
            rel_q = cls.objects.filter(batch_time=n)
            lookup = {x:y for x,y in rel_q.values_list('batch_id','id')}
            
            for q in cls.__queue:
                q.id = lookup[q.batch_id]
                returning.append(q)
        
        del cls.__queue[:]
        return returning
        
    def queue(self):
        self.__class__.add_to_queue(self)
      