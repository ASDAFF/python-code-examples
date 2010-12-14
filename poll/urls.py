from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from asyncore import poll

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^poll/', include('poll.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^/polls/$', 'poll.publicPoll.views.index'),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    )
