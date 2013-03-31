from django.conf.urls import patterns, include, url
import tbpsite

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tbpsite.views.home', name='home'),
    url(r'^poker_tournament$', 'tbpsite.views.poker_tournament'),
    url(r'^rubegoldberg$', 'tbpsite.views.rube_goldberg'),
    url(r'^requirements$', 'tbpsite.views.requirements'),
    #url(r'^candidates$', 'tbpsite.views.candidates'),
    #url(r'^distinguishedactive$', 'tbpsite.views.distinguishedactive'),
    url(r'^awards$', 'tbpsite.views.awards'),
    url(r'^officers$', 'tbpsite.views.officers'),
    url(r'^faculty$', 'tbpsite.views.faculty'),
    url(r'^tutoring$', 'tbpsite.views.tutoring'),
    url(r'^contact$', 'tbpsite.views.contact'),
    url(r'^eligibility_list$', 'tbpsite.views.eligibility_list'),
    url(r'^houses$', 'tbpsite.views.houses'),
    # url(r'^tbpsite/', include('tbpsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
