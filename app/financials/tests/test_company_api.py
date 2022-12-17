"""
Tests for Company APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Company

from financials.serializers import (
    CompanySerializer,
    CompanyDetailSerializer,
)


COMPANIES_URL = reverse('financials:company-list')


def detail_url(company_id):
    """Create and return company detail url."""
    return reverse('financials:company-detail', args=[company_id])


def create_company(**params):
    """Create and return a sample company."""
    defaults = {
        'name_company': 'Apple',
        'symbol': 'AAPL',
        'cik': '0000320193',
        'sector': 'Technology',
        'industry_category': 'Consumer Electronics',
        'company_url': 'https://www.apple.com/',
        'description': 'Apple Inc. designs, manufactures,' +
                'and markets smartphones, personal' +
                'computers, tablets, wearables, and' +
                'accessories worldwide. It also sells' +
                'various related services. In addition,' +
                'the company offers iPhone, a line of' +
                'smartphones; Mac, a line of personal computers;' +
                'iPad, a line of multi-purpose tablets; and' +
                'wearables, home, and accessories comprising AirPods,' +
                'Apple TV, Apple Watch, Beats products, and HomePod.' +
                'Further, it provides AppleCare support and cloud services' +
                'store services; and operates various platforms,' +
                'including the App Store that allow customers to' +
                'discover and download applications and digital content,' +
                'such as books, music, video, games, and podcasts.' +
                'Additionally, the company offers various services,' +
                'such as Apple Arcade, a game subscription service;' +
                'Apple Fitness+, a personalized fitness service;' +
                'Apple Music, which offers users a curated listening' +
                'experience with on-demand radio stations; Apple News+,' +
                'a subscription news and magazine service; Apple TV+,' +
                'which offers exclusive original content; Apple Card,' +
                'a co-branded credit card; and Apple Pay, a cashless' +
                'payment service, as well as licenses its intellectual' +
                'property. The company serves consumers, and small and' +
                'mid-sized businesses; and the education, enterprise,' +
                'and government markets. It distributes third-party' +
                'applications for its products through the App Store.' +
                'The company also sells its products through its retail' +
                'cellular network carriers, wholesalers, retailers, and' +
                'resellers. Apple Inc. was incorporated in 1977 and is' +
                'headquartered in Cupertino, California.',
    }
    defaults.update(params)

    company = Company.objects.create(**defaults)
    return company


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicCompanyApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(COMPANIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCompanyApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_companies(self):
        """Test retrieving a list of Companies."""
        create_company()
        create_company(name_company='Microsoft', symbol='MSFT')

        res = self.client.get(COMPANIES_URL)

        companies = Company.objects.all().order_by('id')
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_company_detail(self):
        """Test get company detail."""
        company = create_company()

        url = detail_url(company.id)
        res = self.client.get(url)

        serializer = CompanyDetailSerializer(company)
        self.assertEqual(res.data, serializer.data)

    def test_create_company(self):
        """Test creating a Company."""
        payload = {
            'name_company': 'Apple',
            'symbol': 'AAPL',
            'cik': '0000320193',
            'sector': 'Technology',
            'industry_category': 'Consumer Electronics',
            'company_url': 'https://www.apple.com/',
            'description': 'Apple Inc. designs, manufactures,' +
                'and markets smartphones, personal' +
                'computers, tablets, wearables, and' +
                'accessories worldwide. It also sells' +
                'various related services. In addition,' +
                'the company offers iPhone, a line of' +
                'smartphones; Mac, a line of personal computers;' +
                'iPad, a line of multi-purpose tablets; and' +
                'wearables, home, and accessories comprising AirPods,' +
                'Apple TV, Apple Watch, Beats products, and HomePod.' +
                'Further, it provides AppleCare support and cloud services' +
                'store services; and operates various platforms,' +
                'including the App Store that allow customers to' +
                'discover and download applications and digital content,' +
                'such as books, music, video, games, and podcasts.' +
                'Additionally, the company offers various services,' +
                'such as Apple Arcade, a game subscription service;' +
                'Apple Fitness+, a personalized fitness service;' +
                'Apple Music, which offers users a curated listening' +
                'experience with on-demand radio stations; Apple News+,' +
                'a subscription news and magazine service; Apple TV+,' +
                'which offers exclusive original content; Apple Card,' +
                'a co-branded credit card; and Apple Pay, a cashless' +
                'payment service, as well as licenses its intellectual' +
                'property. The company serves consumers, and small and' +
                'mid-sized businesses; and the education, enterprise,' +
                'and government markets. It distributes third-party' +
                'applications for its products through the App Store.' +
                'The company also sells its products through its retail' +
                'cellular network carriers, wholesalers, retailers, and' +
                'resellers. Apple Inc. was incorporated in 1977 and is' +
                'headquartered in Cupertino, California.',
        }
        res = self.client.post(COMPANIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        company = Company.objects.get(id=res.data['id'])
        for k,  v in payload.items():
            self.assertEqual(getattr(company, k), v)


    def test_partial_update_company(self):
        """Test partial update of a company."""
        company = create_company()

        payload = {'company_url': 'https://www.apple.com/win',}
        url = detail_url(company.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertEqual(company.company_url, payload['company_url'])

    def test_full_update_company(self):
        """Test full update of company."""
        company = create_company()

        payload = {
            'name_company': 'Aple',
            'symbol': 'APL',
            'cik': '000320193',
            'sector': 'Techno',
            'industry_category': 'Consumer',
            'company_url': 'https://www.apple.co/',
            'description': 'The most valuable firm in the world.',
        }
        url = detail_url(company.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(company, k), v)

    def test_delete_company(self):
        """Test deleting a company successful."""
        company = create_company()

        url = detail_url(company.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company.id).exists())

