"""
Tests for financials APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Company

from financials.serializers import CompanySerializer


COMPANIES_URL = reverse('company:company-list')


def create_company(**params):
    """Create and return a sample company."""
    defaults = {
        'name_company': 'Apple',
        'symbol': 'AAPL',
        'cik': '0000320193',
        'sector': 'Technology',
        'industry_category': 'Consumer Electronics',
        'company_url': 'https://www.apple.com/',
        'description': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. In addition, the company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. Further, it provides AppleCare support and cloud services store services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. Additionally, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was incorporated in 1977 and is headquartered in Cupertino, California.',
    }
    defaults.update(params)

    company = Company.objects.create(**defaults)
    return company


class PublicRecipeAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(COMPANIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_companies(self):
        """Test retrieving a list of Companies"""
        create_company()
        create_company()

        res = self.client.get(COMPANIES_URL)

        companies = Company.objects.all().order_by('-id')
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(res.status, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)