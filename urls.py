from django.conf.urls.defaults import patterns, include, url
from avrora import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()




urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'avrora.views.home', name='home'),
    # url(r'^avrora/', include('avrora.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
#from django.conf import settings
#if settings.DEBUG:
#    urlpatterns+=patterns('django.views.static',
#        url(r'^static/(?P<path>.*)$', 'serve'),
#        )
#shop
urlpatterns+= patterns('avrora.core.views',
                       url(r'^$', 'home', name='avrora_home'),
                       url(r'^upload_csv/$','load_product', name='load_product'),
                       )
urlpatterns+= patterns('avrora.catalog.views',
                       url(r'^catalog/(?P<slug>[-\w]*)/$','category_view', name='category'),
                       url(r'^product/(?P<slug>[-\w]*)/$','product_detail', name='product'),
                       )

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()