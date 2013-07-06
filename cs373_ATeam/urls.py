from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'wcdb.views.index'),
    url(r'^import/$', 'wcdb.views.importView'),
    url(r'^crisis/(?P<crisis_id>\d)$', 'wcdb.views.crisisView'),
    url(r'^orgs/(?P<orgs_id>\d)$', 'wcdb.views.orgsView'),
    url(r'^people/(?P<people_id>\d)$', 'wcdb.views.peopleView'),
    # url(r'^cs373_ATeam/', include('cs373_ATeam.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	
)
