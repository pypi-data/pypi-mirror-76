from django.conf.urls import re_path
from urlshortener import views


app_name = "shortener"

urlpatterns = [
    re_path(r"^list/dashboard/$", views.URLListDashboard.as_view(), name="url_list_dashboard"),
    re_path(r"^create/$", views.URLCreateView.as_view(), name="url_create_view"),
    re_path(r"^(?P<shortcode>[\w-]+)/detail/dashboard/$", views.URLDetailDashboard.as_view(), name="url_detail_dashboard"),
    re_path(r"^(?P<shortcode>[\w-]+)/update/$", views.URLUpdateView.as_view(), name="url_update_view"),
    re_path(r"^(?P<shortcode>[\w-]+)/remove/$", views.URLRemoveView.as_view(), name="url_remove_view"),
]