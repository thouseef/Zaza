from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
                       (r'^$', 'zaza.ui.views.index'),
                       (r'^book/(\d+)/$','zaza.ui.views.book_view'),
                       (r'^book/(\d+)/comment/$','zaza.ui.views.add_comment'),
                       (r'^book/(\d+)/comment/(\d+)/$','zaza.ui.views.edit_comment'),
                       (r'^user/$','zaza.ui.views.user'),
                       (r'^accounts/$','django.contrib.auth.views.login'),
                       (r'^accounts/login/$','django.contrib.auth.views.login'),
                       (r'^accounts/logout/$','django.contrib.auth.views.logout'),
                       (r'^accounts/profile/','zaza.ui.views.user'),
                       (r'^register/$','zaza.ui.views.user_reg'),
                       (r'^admin/', include(admin.site.urls)),

)
