"""
Views for the financials APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Company
from financials import serializers


class CompanyViewSet(viewsets.ModelViewSet):
    """View for manage company APIs."""
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all()
    authentication_classes = [TokenAuthentication]
    Permission_classes = [IsAuthenticated]
