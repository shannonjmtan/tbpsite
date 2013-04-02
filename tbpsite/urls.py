from django.conf.urls import patterns, include, url
import app
import django

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^events$', 'app.views.events'),
    url(r'^poker_tournament$', 'app.views.poker_tournament'),
    url(r'^rubegoldberg$', 'app.views.rube_goldberg'),
    url(r'^requirements$', 'app.views.requirements'),
    url(r'^programs$', 'app.views.programs'),
    url(r'^emcc$', 'app.views.emcc'),
    url(r'^fe$', 'app.views.fe'),
    url(r'^about$', 'app.views.about'),
    url(r'^awards$', 'app.views.awards'),
    url(r'^officers$', 'app.views.officers'),
    url(r'^faculty$', 'app.views.faculty'),
    url(r'^tutoring$', 'app.views.tutoring'),
    url(r'^contact$', 'app.views.contact'),
    url(r'^eligibility_list$', 'app.views.eligibility_list'),
    url(r'^houses$', 'app.views.houses'),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout$', 'app.views.logout'),
    url(r'^login$', 'app.views.login'),
    url(r'^profile$', 'app.views.profile'),
)
