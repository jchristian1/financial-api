"""
Url mappins for Financial APIs.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from financials import views


router  = DefaultRouter()
router.register('company', views.CompanyViewSet)

app_name = 'financials'

urlpatterns = [
    path('', include(router.urls)),
]