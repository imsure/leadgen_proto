from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activity_patterns', views.ActivityPatternViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^activity_patterns/(?P<pk>[0-9]+)/travel_options/(?P<mode>[a-z_]+)/$', views.travel_option),
    url(r'^', include(router.urls)),
]
