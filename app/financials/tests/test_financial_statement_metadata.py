"""
Test for Financial statements meta data APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    StatementMetaData,
    Statement,
    Company,
)

from financials.serializers import (
    StatementMetaDataSerializer,
)

import hashlib


STATEMENT_META_DATA_URL = reverse('financials:statementmetadata-list')


def detail_url(financial_statement_meta_data_id):
    """Create and return a financial statement metadata detail url."""
    return reverse('financials:statementmetadata-detail', args=[financial_statement_meta_data_id])


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


def create_statement(**params):
    """Create and return a new statement."""
    defaults = {
        'statement_name': 'Cash Flow Statement'
    }
    defaults.update(params)

    statement = Statement.objects.create(**defaults)
    return statement


def create_financial_statement_meta_data(**params):
    """Create new financial statement meta data"""
    defaults = {
        'name_company': 'APPLE',
        'symbol': 'AAPL',
        'cik': '0000320193',
        'sector': 'Technology',
        'industry_category': 'Consumer Electronics',
        'company_url': 'https://www.apple.com',
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

    defaults = {
        'statement_name': 'Cash Flow Statement Standarized'
    }
    statement_type = Statement.objects.create(**defaults)

    if params:
        unique_hash = '2022-09-24' + company.symbol + 'FY' + 'Cash Flow Statement Standarized'
    else :
        unique_hash = '2022-09-24AAPLFYCash Flow Statement Standarized'

    statement_meta_data = StatementMetaData.objects.create(
            unique_hash = hashlib.sha256(unique_hash.encode()).hexdigest(),
            id_company = company,
            id_statement_type = statement_type,
            fiscal_year = '2022',
            fiscal_period = 'FY',
            filling_date = '2022-10-28',
            start_date = '2022-09-24',
            end_date = '2022-10-27',
            url = 'https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/0000320193-22-000108-index.htm',
            urlfinal = 'https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm',
            unit = 'USD',)
    return statement_meta_data


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicStatementApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(STATEMENT_META_DATA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateStatementApiTests(TestCase):
    """Tests for authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_statements_meta_data(self):
        """Test for retrieving statements meta data."""
        create_financial_statement_meta_data()
        create_financial_statement_meta_data()
        create_financial_statement_meta_data(
            name_company='MICROSOFT',
            symbol='MSFT',
        )

        res = self.client.get(STATEMENT_META_DATA_URL)

        statement_meta_data = StatementMetaData.objects.all().order_by('id')
        serializer = StatementMetaDataSerializer(statement_meta_data, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_statements_meta_data_detail(self):
        """Test get Statement metadata detail."""
        statement_meta_data = create_financial_statement_meta_data(
            name_company='TESLA',
            symbol='TSLA',
        )

        url = detail_url(statement_meta_data.id)
        res = self.client.get(url)

        serializer = StatementMetaDataSerializer(statement_meta_data)
        self.assertEqual(res.data, serializer.data)

    def test_create_statements_meta_data(self):
        """Test create Statement meta data."""
        statement = create_statement()
        company = create_company(
            name_company='NETFLIX',
            symbol='NFLX',
        )
        unique_hash = '2022-09-24NFLXFYCash Flow Statement Standarized'
        payload = {
            'unique_hash': hashlib.sha256(unique_hash.encode()).hexdigest(),
            'id_company': company.id,
            'id_statement_type': statement.id,
            'fiscal_year': '2022',
            'fiscal_period': 'FY',
            'filling_date': '2022-10-28',
            'start_date': '2022-09-24',
            'end_date': '2022-10-27',
            'url': 'https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/0000320193-22-000108-index.htm',
            'urlfinal': 'https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm',
            'unit': 'USD',
        }
        res = self.client.post(STATEMENT_META_DATA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        statements_meta_data = StatementMetaData.objects.get(id=res.data['id'])
        self.assertEqual(statements_meta_data.unique_hash, payload['unique_hash'])

    def test_partial_update(self):
        """Test partial update of a financial statement metadata"""
        statement_meta_data = create_financial_statement_meta_data(
            name_company='TESLA',
            symbol='TSLA',
        )
        payload = {
            'filling_date': '2022-11-28',
            'start_date': '2022-10-24',
        }
        url = detail_url(statement_meta_data.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        statement_meta_data.refresh_from_db()
        self.assertEqual(str(statement_meta_data.filling_date), payload['filling_date'])
        self.assertEqual(str(statement_meta_data.start_date), payload['start_date'])

    def test_delete_statement_meta_data(self):
        """Test for deleting financial statements metadata."""
        statement_meta_data = create_financial_statement_meta_data(
            name_company='NVIDIA',
            symbol='NVDA',
        )

        url = detail_url(statement_meta_data.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(StatementMetaData.objects.filter(id=statement_meta_data.id).exists())