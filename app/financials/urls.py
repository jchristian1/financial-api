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
router.register('companies', views.CompanyViewSet)
router.register('indicators', views.IndicatorViewSet)
router.register('statements', views.StatementViewSet)
router.register('statementmetadatas', views.StatementMetaDataViewSet)

app_name = 'financials'

urlpatterns = [
    path('', include(router.urls)),
]

"""for pattern in router.urls:
    print(pattern.pattern.regex.pattern)"""