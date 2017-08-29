from __future__ import print_function
from __future__ import unicode_literals

from django.conf.urls import url
from djangolg import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="djangolg-index"),
    url(r'^enter/$', views.AcceptTermsView.as_view(), name="djangolg-enter"),
    url(r'^lg/$', views.LookingGlassJsonView.as_view(), name="djangolg-lg"),
]
