from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()


urlpatterns = patterns('',
                       (r'^$', 'zaza.ui.views.index'),
                       (r'^static/(?P<path>.*)$','django.views.static.serve',
                        {'document_root': settings.STATIC_DOC_ROOT,'show_indexes': True}),
                       (r'^book/(\w+)/$','zaza.ui.views.book_view'),
                       (r'^book/(\w+)/comment/$','zaza.ui.views.add_comment'),
                       (r'^book/(\w+)/comment/(\d+)','zaza.ui.views.edit_comment'),
                       (r'^book/(\w+)/rating/$','zaza.ui.views.view_rating'),
                       (r'^book/(\w+)/rate/(\d+)$','zaza.ui.views.add_rating'),
                       (r'^book/(\w+)/deleterating/$', 'zaza.ui.views.del_rating'),
                       (r'^user/$','zaza.ui.views.user'),
                       (r'^user/books','zaza.ui.views.book_rated'),
                       (r'^search/$', 'zaza.ui.views.search'),
                       (r'^accounts/$','django.contrib.auth.views.login'),
                       (r'^accounts/login/$','django.contrib.auth.views.login'),
                       (r'^accounts/logout/$','zaza.ui.views.logout'),
                       (r'^accounts/profile/','zaza.ui.views.user'),
                       (r'^accounts/profile/update/','zaza.ui.views.user_update'),
                       (r'^accounts/(\w+)/$', 'zaza.ui.views.other_user'),
                       (r'^register/$','zaza.ui.views.user_reg'),
                       (r'^register/success/$','zaza.ui.views.user_reg'),
                       (r'^admin/', include(admin.site.urls)),

)
