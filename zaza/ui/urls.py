from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()


urlpatterns = patterns('',
                       (r'^$', 'zaza.ui.views.index'),
                       (r'^static/(?P<path>.*)$','django.views.static.serve',
                        {'document_root': settings.STATIC_DOC_ROOT,'show_indexes': True}),
                       (r'^book/(\d+)/$','zaza.ui.views.book_view'),
                       (r'^book/(\d+)/comment/$','zaza.ui.views.add_comment'),
                       (r'^book/(\d+)/comment/(\d+)','zaza.ui.views.edit_comment'),
                       (r'^book/(\d+)/rating/$','zaza.ui.views.view_rating'),
                       (r'^book/(\d+)/rate/(\d+)$','zaza.ui.views.add_rating'),
                       (r'^user/$','zaza.ui.views.user'),
                       (r'^accounts/$','django.contrib.auth.views.login'),
                       (r'^accounts/login/$','django.contrib.auth.views.login'),
                       (r'^accounts/logout/$','django.contrib.auth.views.logout'),
                       (r'^accounts/profile/','zaza.ui.views.user'),
                       (r'^register/$','zaza.ui.views.user_reg'),
                       (r'^admin/', include(admin.site.urls)),

)
