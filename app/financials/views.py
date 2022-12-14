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
    StatementMetaData,
    FinancialValue,
)

from financials import serializers

from django.db import IntegrityError


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
        """Create a new Company."""
        try:
            company = serializer.save()
        except IntegrityError:
            pass
        else:
            return company


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

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.StatementMetaDataSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Financial statement meta data."""
        try:
            statement_meta_data = serializer.save()
        except IntegrityError:
            pass
        else:
            return statement_meta_data


class FinancialValuesViewSet(viewsets.ModelViewSet):
    """Views for manage the  financial statement meta data APIs."""
    serializer_class = serializers.FinancialValueSerializer
    queryset = FinancialValue.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

