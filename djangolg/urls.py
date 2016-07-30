from django.conf.urls import url
from djangolg import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="djangolg-index"),
    url(r'^lg/(?P<method>\w+)/$', views.LookingGlassHTMLView.as_view(), name="djangolg-lg"),
]
