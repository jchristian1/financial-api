"""
Tests for financial statement APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Statement

from financials.serializers import StatementSerializer


STATEMENT_URL = reverse('financials:statement-list')


def create_statement(**params):
    """Create and return a new statement."""
    defaults = {
        'statement_name': 'Cash Flow Statement'
    }
    defaults.update(params)

    statement = Statement.objects.create(**defaults)
    return statement

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicStatementApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(STATEMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStatementApiTests(TestCase):
    """Tests for authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_statements(self):
        """Test for retrieving statements."""
        create_statement()
        create_statement(statement_name='Profit and Loss Statement')

        res = self.client.get(STATEMENT_URL)

        statement = Statement.objects.all().order_by('id')
        serializer = StatementSerializer(statement, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

