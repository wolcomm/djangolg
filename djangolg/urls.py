from django.conf.urls import url
from djangolg import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="djangolg-index"),
    url(r'^enter/$', views.AcceptTermsView.as_view(), name="djangolg-enter"),
    url(r'^lg/$', views.LookingGlassHTMLView.as_view(), name="djangolg-lg"),
]
