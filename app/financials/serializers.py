"""
Serializers for financials APIs.
"""
from rest_framework import serializers

from core.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for financials."""

    class Meta:
        model = Company
        fields = [
            'id', 'name_company', 'symbol', 'cik', 'sector',
            'industry_category', 'company_url',
        ]
        read_only_fields = ['id']

class CompanyDetailSerializer(CompanySerializer):
    """Serializer for recipes."""

    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + ['description']
