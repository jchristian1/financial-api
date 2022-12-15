"""
Serializers for financials APIs.
"""
from rest_framework import serializers

from core.models import (
    Company,
    FinancialIndicator,
)


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company."""

    class Meta:
        model = Company
        fields = [
            'id', 'name_company', 'symbol', 'cik', 'sector',
            'industry_category', 'company_url',
        ]
        read_only_fields = ['id']


class CompanyDetailSerializer(CompanySerializer):
    """Serializer for Company details."""

    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + ['description']


class FinancialIndicatorSerializer(serializers.ModelSerializer):
    """Serializer for financial indicator."""

    class Meta:
        model = FinancialIndicator
        fields = ['indicator_name', 'tag']
        read_only_fields = ['id']


class FinancialIndicatorDetailSerializer(FinancialIndicatorSerializer):
    """Serializer for financial indicator details."""

    class Meta:
        fields = FinancialIndicatorSerializer.Meta.fields + ['description']



