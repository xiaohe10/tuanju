from django.conf.urls import patterns, include, url

from django.contrib import admin
from tuanju.settings import MEDIA_ROOT

from web.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT}),

    url(r'^$',organizations),
    url(r'^cube$',get_cubes),
    url(r'^organizations$',organizations),
    url(r'^departments$',departments),
    url(r'^zhibu$',zhibu),
    url(r'^surround$',surround),
    url(r'^login$',my_login),
    url(r'^logout$',my_logout),
    url(r'^add$',add),
    url(r'^delete$',delete),
    url(r'^modify$',modify),
    url(r'^up$',up),
    url(r'^down$',down),


    url(r'^admin/', include(admin.site.urls)),
)
