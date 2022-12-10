"""
Url mappings for Financial APIs.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from financials import views


router = DefaultRouter()
router.register('companies', views.CompanyViewSet)

app_name = 'company'

urlpatterns = [
    path('', include(router.urls)),
]
