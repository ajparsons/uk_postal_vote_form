from django.conf.urls import patterns, include, url
from django.contrib import admin
from vote import views

from useful_inkleby.useful_django.views import AppUrl

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),    
        ]

urlpatterns += AppUrl('vote.views').patterns()
