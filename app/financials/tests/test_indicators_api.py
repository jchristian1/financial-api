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

def detail_url(indicator_url):
    """Create and return a financial indicator detail URL."""
    return reverse('financials:indicator-detail', args=[indicator_url])


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


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com', password='testpass123')
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

    def test_get_indicator_detail(self):
        """Test get indicator detail."""
        indicator = create_indicator()

        url = detail_url(indicator.id)
        res = self.client.get(url)

        serializer = IndicatorSerializer(indicator)
        self.assertEqual(res.data, serializer.data)


    def test_create_indicator(self):
        """Test creating a financial indicator."""
        payload = {
            'description': 'Costs',
            'indicator_name': 'Costs',
            'tag': 'Costs',
        }
        res = self.client.post(INDICATOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        indicator = Indicator.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(indicator, k), v)

    def test_partial_update(self):
        """Test Partial update of indicator."""
        indicator = create_indicator(
            description='revenue',
            indicator_name='Revenue',
            tag='revenue',
        )

        payload = {'description': 'Earnings'}
        url = detail_url(indicator.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        indicator.refresh_from_db()
        self.assertEqual(indicator.description, payload['description'])
        self.assertEqual(indicator.tag, 'revenue')

    def test_full_update_indicator(self):
        """Test delete financial indicator."""
        indicator = create_indicator(
            description = 'Costs',
            indicator_name = 'Costs',
            tag = 'Costs',
        )

        payload = {
            'description': 'Costs',
            'indicator_name': 'Costs',
            'tag': 'Costs',
        }
        url = detail_url(indicator.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        indicator.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(indicator, k), v)

    def test_delete_indicator(self):
        """Test to delete an indicator."""
        indicator = create_indicator()

        url = detail_url(indicator.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
