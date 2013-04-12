from django.conf.urls import patterns, include, url
import main
import django

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^events$', 'main.views.events'),
    url(r'^poker_tournament$', 'main.views.poker_tournament'),
    url(r'^rubegoldberg$', 'main.views.rube_goldberg'),
    url(r'^requirements$', 'main.views.requirements'),
    url(r'^programs$', 'main.views.programs'),
    url(r'^emcc$', 'main.views.emcc'),
    url(r'^fe$', 'main.views.fe'),
    url(r'^about$', 'main.views.about'),
    url(r'^awards$', 'main.views.awards'),
    url(r'^officers$', 'main.views.officers'),
    url(r'^faculty$', 'main.views.faculty'),
    url(r'^tutoring$', 'main.views.tutoring'),
    url(r'^feedback$', 'main.views.feedback'),
    url(r'^contact$', 'main.views.contact'),
    url(r'^eligibility_list$', 'main.views.eligibility_list'),
    url(r'^houses$', 'main.views.houses'),
    # url(r'^app/', include('main.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout$', 'main.views.logout'),
    url(r'^login$', 'main.views.login'),
    url(r'^profile$', 'main.views.profile'),
    url(r'^resume$', 'main.views.resume'),
    url(r'^interview$', 'main.views.interview'),
)
