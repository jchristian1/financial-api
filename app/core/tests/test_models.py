"""
Test for models.
date='2022-09-24',
            symbol='AAPL',
            reportedCurrency='USD',
            cik='0000320193',
            fillingDate='2022-10-28',
            acceptedDate='2022-10-27 18:01:14',
            calendarYear='2022',
            period='FY',
            netIncome=99803000000,
            depreciationAndAmortization=11104000000,
            deferredIncomeTax=895000000,
            stockBasedCompensation=9038000000,
            changeInWorkingCapital=1200000000,
            accountsReceivables=-1823000000,
            inventory=1484000000,
            accountsPayables=9448000000,
            otherWorkingCapital=478000000,
            otherNonCashItems=111000000,
            netCashProvidedByOperatingActivities=122151000000,
            investmentsInPropertyPlantAndEquipment=-10708000000,
            acquisitionsNet=-306000000,
            purchasesOfInvestments=-76923000000,
            salesMaturitiesOfInvestments=67363000000,
            otherInvestingActivites=-1780000000,
            netCashUsedForInvestingActivites=-22354000000,
            debtRepayment=-9543000000,
            commonStockIssued=0.0,
            commonStockRepurchased=-89402000000,
            dividendsPaid =14841000000,
            otherFinancingActivites=3037000000,
            netCashUsedProvidedByFinancingActivities=-110749000000,
            effectOfForexChangesOnCash=0.0,
            netChangeInCash=-10952000000,
            cashAtEndOfPeriod=24977000000,
            cashAtBeginningOfPeriod=35929000000,
            operatingCashFlow=122151000000,
            capitalExpenditure=-10708000000,
            freeCashFlow=111443000000,
            link="https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/0000320193-22-000108-index.htm",
            finalLink="https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm"
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

import hashlib


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Tesr creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_company(self):
        """Test creating a company is successful."""

        company = models.Company.objects.create(
            name_company='APPLE',
            symbol='AAPL',
            cik='0000320193',
            sector='Technology',
            industry_category='Consumer Electronics',
            company_url='https://www.apple.com',
            description='Apple Inc. designs, manufactures,' +
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
        )

        self.assertEqual(str(company), company.name_company)

    def test_create_financial_indicator(self):
        """Test create financial indicator API."""
        financial_indicator = models.Indicator.objects.create(
            description='Revenue is the total amount of income' +
            ' generated by the sale of goods or services related' +
            ' to the companys primary operations. Revenue, also' +
            ' known as gross sales, is often referred to as the' +
            ' top line because it sits at the top of the income' +
            ' statement.',
            indicator_name='Revenue',
            tag='revenue',
        )

        self.assertEqual(
            str(financial_indicator),
            financial_indicator.indicator_name,
        )

    def test_create_financial_statement_type(self):
        """Test create financial indicator type."""
        financial_statement = models.Statement.objects.create(
            statement_name='Proffit and Loss Statement',
        )

        self.assertEqual(
            str(financial_statement),
            financial_statement.statement_name
        )

    def test_create_financial_statement_meta_data(self):
        """Test create financial statement meta data."""
        company = models.Company.objects.create(
            name_company='APPLE',
            symbol='AAPL',
            cik='0000320193',
            sector='Technology',
            industry_category='Consumer Electronics',
            company_url='https://www.apple.com',
            description='Apple Inc. designs, manufactures,' +
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
        )
        statement_type = models.Statement.objects.create(
            statement_name='Balance Sheet Statement Standarized'
        )

        date = '2022-09-24'
        ticker = company.symbol
        period = 'FY'
        statement_name = statement_type.statement_name
        data = date + ticker + period + statement_name
        statement_meta_data = models.StatementMetaData.objects.create(
            unique_hash=hashlib.sha256(data.encode()).hexdigest(),
            id_company=company,
            id_statement_type=statement_type,
            fiscal_year='2022',
            fiscal_period='FY',
            filling_date='2022-10-28',
            start_date='2022-09-24',
            end_date='2022-10-27',
            url='https://www.sec.gov/Archives/edgar/' +
                'data/320193/000032019322000108/' +
                '0000320193-22-000108-index.htm',
            urlfinal='https://www.sec.gov/Archives/edgar' +
                     '/data/320193/000032019322000108/aapl-20220924.htm',
            unit='USD',
        )

        self.assertEqual(
            str(statement_meta_data),
            f'{company.name_company} - {statement_type.statement_name} - {statement_meta_data.start_date} - {statement_meta_data.fiscal_period}'
        )

    def test_create_financial_value(self):
        """Test fo creating a financial value, welcome to the heart."""

        company = models.Company.objects.create(
            name_company='APPLE',
            symbol='AAPL',
            cik='0000320193',
            sector='Technology',
            industry_category='Consumer Electronics',
            company_url='https://www.apple.com',
            description='Apple Inc. designs, manufactures,' +
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
        )
        statement_type = models.Statement.objects.create(
            statement_name='Balance Sheet Statement Standarized'
        )
        indicator = models.Indicator.objects.create(
             description='Revenue is the total amount of income' +
            ' generated by the sale of goods or services related' +
            ' to the companys primary operations. Revenue, also' +
            ' known as gross sales, is often referred to as the' +
            ' top line because it sits at the top of the income' +
            ' statement.',
            indicator_name='Revenue',
            tag='revenue',
        )

        date = '2022-09-24'
        ticker = company.symbol
        period = 'FY'
        statement_name = statement_type.statement_name
        data = date + ticker + period + statement_name
        statement_meta_data = models.StatementMetaData.objects.create(
            unique_hash=hashlib.sha256(data.encode()).hexdigest(),
            id_company=company,
            id_statement_type=statement_type,
            fiscal_year='2022',
            fiscal_period='FY',
            filling_date='2022-10-28',
            start_date='2022-09-24',
            end_date='2022-10-27',
            url='https://www.sec.gov/Archives/edgar/' +
                'data/320193/000032019322000108/' +
                '0000320193-22-000108-index.htm',
            urlfinal='https://www.sec.gov/Archives/edgar' +
                     '/data/320193/000032019322000108/aapl-20220924.htm',
            unit='USD',
        )

        values = models.FinancialValue.objects.create(
            id_financial_statement_meta_data = statement_meta_data,
            id_Financial_Indicator = indicator,
            ammount = 23646000000,
        )

        self.assertEqual(
            str(values),
            f'{values.id_financial_statement_meta_data} - {indicator.indicator_name} - {values.ammount}'
        )