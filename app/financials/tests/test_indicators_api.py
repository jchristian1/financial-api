"""
Tests for financial indicators APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Indicator

from financials.serializers import IndicatorSerializer


INDICATOR_URL = reverse('financials:indicator-list')


def create_indicator(**params):
    """Create and return a sample of a financial indicator."""
    defaults = {
        'description': 'revenue',
        'indicator_name': 'Revenue',
        'tag':'revenue',
    }
    defaults.update(params)

    indicator = Indicator.objects.create(**defaults)
    return indicator


class PublicIndicatorApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(INDICATOR_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIndicatorApiTests(TestCase):
    """Test retrieving a list of recipes."""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_indicators(self):
        """Test retrieving a list of recipes."""
        create_indicator()
        create_indicator()

        res = self.client.get(INDICATOR_URL)

        indicator = Indicator.objects.all().order_by('id')
        serializer = IndicatorSerializer(indicator, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


