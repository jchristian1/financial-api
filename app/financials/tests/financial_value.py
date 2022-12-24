"""
Test for the financial values APIs.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Company,
    Statement,
    StatementMetaData,
    FinancialValue,
    Indicator,
)

from financials.serializers import FinancialValueSerializer

import hashlib


VALUES_URL = reverse('financials:financialvalue-list')


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


    defaults.update(params)
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


def create_indicator(**params):
    """Create a new indicator."""

    defaults = {
        'description': 'Cash in banks or temporary investments',
        'indicator_name': 'Cash And Cash And Equivalents',
        'tag': 'CashAndCashAndEquivalents',
    }
    defaults.update(params)

    indicator = Indicator.objects.create(**defaults)
    return indicator

def create_value(**params):
    """Creating new value."""
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
    statement_type = create_statement()

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

    indicator = create_indicator()

    value = FinancialValue.objects.create(
        id_financial_statement_meta_data= statement_meta_data,
        id_Financial_Indicator= indicator,
        ammount= 10000000000,
    )

    return value


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)



class PublicStatementApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(VALUES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateStatementApiTests(TestCase):
    """Tests for authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_statements_meta_data(self):
        """Test for retrieving statements meta data."""
        create_value()
        create_value()

        res = self.client.get(VALUES_URL)

        values = FinancialValue.objects.all().order_by('id')
        serializer = FinancialValueSerializer(values, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
