from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from django.views.generic.create_update import delete_object
from django.contrib.auth.decorators import permission_required

from archweb_dev.main.models import Todolist

admin.autodiscover()

urlpatterns = patterns('',
# Dynamic Stuff
    (r'^packages/unflag/(\d+)/$',        'archweb_dev.packages.views.unflag'),
    (r'^packages/files/(\d+)/$',         'archweb_dev.packages.views.files'),
    (r'^packages/signoffs/$',              'archweb_dev.packages.views.signoffs'),
    (r'^packages/signoff_package/(?P<arch>[A-z0-9]+)/(?P<pkgname>[A-z0-9\-+.]+)/$',
        'archweb_dev.packages.views.signoff_package'),
    (r'^packages/search/$',              'archweb_dev.packages.views.search'),
    (r'^packages/search/([A-z0-9]+)/$',  'archweb_dev.packages.views.search'),
    (r'^packages/update/$',              'archweb_dev.packages.views.update'),
    (r'^packages/(?P<pkgid>\d+)/$',      'archweb_dev.packages.views.details'),
    (r'^packages/(?P<name>[A-z0-9]+)/$', 'archweb_dev.packages.views.details'),
    (r'^packages/(?P<repo>[A-z0-9]+)/(?P<name>[A-z0-9\-+.]+)/$',
        'archweb_dev.packages.views.details'),
    (r'^packages/(?P<repo>[A-z0-9]+)/(?P<arch>[A-z0-9]+)/(?P<name>[A-z0-9\-+.]+)/$',
        'archweb_dev.packages.views.details'),
    (r'^packages/$',                     'archweb_dev.packages.views.search'),

    (r'^todo/(\d+)/$',              'archweb_dev.todolists.views.view'),
    (r'^todo/add/$',                'archweb_dev.todolists.views.add'),
    (r'^todo/edit/(?P<list_id>\d+)/$',  'archweb_dev.todolists.views.edit'),
    (r'^todo/flag/(\d+)/(\d+)/$',   'archweb_dev.todolists.views.flag'),
    (r'^todo/delete/(?P<object_id>\d+)/$', permission_required(
        'main.delete_todolist')(delete_object), {
            'model': Todolist,
            'template_name': 'todolists/todolist_confirm_delete.html',
            'post_delete_redirect': '/todo/'
        }),
    (r'^todo/$',                    'archweb_dev.todolists.views.list'),

    (r'^news/(\d+)/$',         'archweb_dev.news.views.view'),
    (r'^news/add/$',           'archweb_dev.news.views.add'),
    (r'^news/edit/(\d+)/$',    'archweb_dev.news.views.edit'),
    (r'^news/delete/(\d+)/$',  'archweb_dev.news.views.delete'),
    (r'^news/$',               'archweb_dev.news.views.list'),

    (r'^devel/$',          'archweb_dev.devel.views.index'),
    (r'^devel/notify/$',   'archweb_dev.devel.views.change_notify'),
    (r'^devel/profile/$',  'archweb_dev.devel.views.change_profile'),

# (mostly) Static Pages
    (r'^$',                'archweb_dev.devel.views.siteindex'),
    (r'^cvs/$',            'archweb_dev.devel.views.cvs'),
    (r'^developers/$',     'archweb_dev.devel.views.developers'),
    (r'^fellows/$',        'archweb_dev.devel.views.fellows'),
    (r'^donate/$',         'archweb_dev.devel.views.donate'),
    (r'^download/$',       'archweb_dev.devel.views.download'),
    (r'^projects/$',       'archweb_dev.devel.views.projects'),
    (r'^robots.txt$',      'archweb_dev.devel.views.robots'),

# Authentication / Admin
    (r'^denied/$',          'archweb_dev.devel.views.denied'),
    (r'^login/$',           'django.contrib.auth.views.login',  {'template_name': 'registration/login.html'}),
    (r'^accounts/login/$',  'django.contrib.auth.views.login',  {'template_name': 'registration/login.html'}),
    (r'^logout/$',          'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG == True:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', 
            {'document_root': settings.DEPLOY_PATH+'/media'}))

# vim: set ts=4 sw=4 et:

