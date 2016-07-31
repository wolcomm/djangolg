from django.conf.urls import url
from djangolg import views

urlpatterns = [
    url(r'^$', views.NewIndexView.as_view(), name="djangolg-index"),
    url(r'^lg/(?P<method>\w+)/$', views.NewLookingGlassHTMLView.as_view(), name="djangolg-lg"),
]
