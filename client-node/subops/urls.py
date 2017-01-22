from django.conf.urls import patterns, include, url
from ops.views import check_name,save_script,run_scripts,script_names

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subops.views.home', name='home'),
    # url(r'^subops/', include('subops.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^check_name/$', check_name),
    (r'^save_script/$', save_script),
    (r'run_scripts',run_scripts),
    (r'script_names',script_names),
)

