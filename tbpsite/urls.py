from django.conf.urls import patterns, include, url
import tbpsite
import django

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tbpsite.views.home', name='home'),
    url(r'^events$', 'tbpsite.views.events'),
    url(r'^poker_tournament$', 'tbpsite.views.poker_tournament'),
    url(r'^rubegoldberg$', 'tbpsite.views.rube_goldberg'),
    url(r'^requirements$', 'tbpsite.views.requirements'),
    url(r'^programs$', 'tbpsite.views.programs'),
    url(r'^emcc$', 'tbpsite.views.emcc'),
    url(r'^fe$', 'tbpsite.views.fe'),
    url(r'^about$', 'tbpsite.views.about'),
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
    url(r'^logout$', 'tbpsite.views.logout'),
    url(r'^login', 'tbpsite.views.login'),
)
