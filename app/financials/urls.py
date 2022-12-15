"""
Url mappings for Financials APIs.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from financials import views


router = DefaultRouter()
router.register('indicators', views.FinancialIndicatorViewSet)
router.register('companies', views.CompanyViewSet)

app_name = 'financials'

urlpatterns = [
    path('', include(router.urls)),
]
