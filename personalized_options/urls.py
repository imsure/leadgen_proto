from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activity_patterns', views.ActivityPatternViewSet)

urlpatterns = [
    # url(r'^activity_patterns/$', views.ActivityPatternList.as_view()),
    url(r'^', include(router.urls)),
]
