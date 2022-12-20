"""
Serializers for financials APIs.
"""
from rest_framework import serializers

from core.models import (
    Company,
    Indicator,
    Statement,
    StatementMetaData
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


class IndicatorSerializer(serializers.ModelSerializer):
    """Serializer for financial indicators."""

    class Meta:
        model = Indicator
        fields = ['id', 'description', 'indicator_name', 'tag']
        read_only_fields = ['id']


class IndicatorDetailSerializer(IndicatorSerializer):
    """Serializer for financial inficator detail view."""

    class Meta:
        fields = IndicatorSerializer.Meta.fields + ['description']


class StatementSerializer(serializers.ModelSerializer):
    """Serializer for the Financial Statement Type."""

    class Meta:
        model = Statement
        fields = ['id', 'statement_name']
        read_only_fields = ['id']

class StatementMetaDataSerializer(serializers.ModelSerializer):
    """Serializer for the Financial Statement Meta Data."""

    class Meta:
        model = StatementMetaData
        fields = ['id', 'unique_hash', 'id_company', 'id_statement_type',
                'fiscal_year', 'fiscal_period', 'filling_date', 'start_date',
                'end_date', 'url', 'urlfinal', 'unit',
        ]