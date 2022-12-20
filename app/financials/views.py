"""
Views for the financials APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import (
    Company,
    Indicator,
    Statement,
    StatementMetaData
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

class IndicatorViewSet(viewsets.ModelViewSet):
    """View for manage financial indicators APIs."""
    serializer_class = serializers.IndicatorSerializer
    queryset = Indicator.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for the request."""
        if self.action == 'list':
            return serializers.IndicatorSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Financial indicator. """
        serializer.save()


class StatementViewSet(viewsets.ModelViewSet):
    """Views for manage the statement APIs."""
    serializer_class = serializers.StatementSerializer
    queryset = Statement.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for the request."""
        if self.action == 'list':
            return serializers.StatementSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Financial statement type. """
        serializer.save()

class StatementMetaDataViewSet(viewsets.ModelViewSet):
    """Views for manage the  financial statement meta data APIs."""
    serializer_class = serializers.StatementMetaDataSerializer
    queryset = StatementMetaData.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]