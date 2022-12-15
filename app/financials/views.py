"""
Views for the financials APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import (
    Company,
    FinancialIndicator,
)

from financials import serializers


class CompanyViewSet(viewsets.ModelViewSet):
    """View for manage company APIs."""
    serializer_class = serializers.CompanyDetailSerializer
    queryset = Company.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.CompanySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Company. """
        serializer.save()

class FinancialIndicatorViewSet(viewsets.ModelViewSet):
    """View for manage Financial Indicators APIs."""
    serializer_class = serializers.FinancialIndicatorSerializer
    queryset = FinancialIndicator.objects.all()
