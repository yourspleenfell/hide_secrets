from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^register$', views.create_user),
    url(r'^dashboard/(?P<id>\d+)$', views.show_user, name="user"),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wish_items/create$', views.create_item),
    url(r'^wish_items/submit/(?P<id>\d+)$', views.submit_item),
    url(r'^wish_items/add/(?P<id>\d+)$', views.add_item),
    url(r'^wish_items/remove/(?P<id>\d+)$', views.remove_item),
    url(r'^wish_items/delete/(?P<id>\d+)$', views.delete_item),
    url(r'^wish_items/(?P<id>\d+)$', views.show_item),
    url(r'^user/(?P<id>\d+)$', views.show_user_list, name="user_list"),
    url(r'^user/(?P<id>\d+)/edit$', views.update_user, name="update_user"),
    url(r'^user/(?P<id>\d+)/update$', views.submit_update),
]