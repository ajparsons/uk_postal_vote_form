from django.conf.urls import include, url
from django.contrib import admin
from postalvote import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', views.postal_vote_form_view),   	
        ]