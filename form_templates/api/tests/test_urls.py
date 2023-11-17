# mypy: disable-error-code="attr-defined"
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from tinydb import Query, TinyDB

User = get_user_model()


class ApiURLTests(TestCase):
    """Test api app."""

    @classmethod
    def setUpClass(cls) -> None:
        """Create test data."""
        super().setUpClass()
        get_form_url = reverse('api:get_form')
        cls.urls = {
            'get_empty_form': get_form_url,
            'get_form_by_name': get_form_url + '?name=ABCDEF',
            'get_form_by_phone': get_form_url
            + '?user_phone=%2B7%20999+999+99+99',
            'get_form_by_email': get_form_url + '?user_email=ABCDEF@mail.ru',
            'get_form_by_date': get_form_url + '?user_date=13.12.1990',
            'get_form_by_dash_date': get_form_url + '?user_date=1990-12-13',
            'get_form_by_text': get_form_url + '?user_text=test%20text_1',
            'get_form_by_unique_together': get_form_url
            + '?user_phone=%2B7%20999+999+99+99&user_email=ABCDEF@mail.ru',
            'missing': '/test/missing_url',
            'get_form_by_all': get_form_url
            + (
                '?user_phone=%2B7%20999+999+99+99'
                '&user_email=ABCDEF@mail.ru'
                '&user_date=1990-12-13'
                '&user_text=test%20text_1'
            ),
        }
        cls.test_database = TinyDB(settings.DATA_STORAGE_LOCATION)
        cls.test_database.insert_multiple(
            [
                {
                    'name': 'object_1',
                    'user_phone': '+7 999 999 99 99',
                    'user_email': 'ABCDEF@mail.ru',
                    'user_date': '13.12.1990',
                    'user_text': 'test text_1',
                },
                {
                    'name': 'object_2',
                    'user_phone': '+7 111 111 11 11',
                    'user_email': 'XUZ2000@mail.ru',
                    'user_date': '01.01.2000',
                    'user_text': 'test text_2',
                },
                {
                    'name': 'object_mixed',
                    'user_phone': '+7 999 999 99 99',
                    'user_email': 'XUZ2000@mail.ru',
                    'user_date': '21.12.2012',
                    'user_text': 'test text_3',
                },
            ],
        )
        cls.query = Query()
        cls.client = Client()

    def test_httpstatuses(self) -> None:
        """Test url status codes."""
        get_form_url = self.urls.get('get_empty_form')
        self.assertEqual(
            self.client.post(get_form_url).status_code,
            HTTPStatus.OK,
        )
        self.assertEqual(
            self.client.get(get_form_url).status_code,
            HTTPStatus.METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(self.urls.get('missing')).status_code,
            HTTPStatus.NOT_FOUND,
        )

    def test_empty_request_values(self) -> None:
        """Test values in response without query parameters."""
        self.assertIn(
            {'name': 'object_1'},
            self.client.post(self.urls.get('get_empty_form')).json(),
        )
        self.assertIn(
            {'name': 'object_2'},
            self.client.post(self.urls.get('get_empty_form')).json(),
        )

    def test_request_with_name_error(self) -> None:
        """Test values in response with specified name."""
        self.assertEqual(
            self.client.post(self.urls.get('get_form_by_name')).json(),
            {'name': "you can't search by name field"},
        )

    def test_request_with_phone(self) -> None:
        """Test values in response with specified phone."""
        result = self.client.post(self.urls.get('get_form_by_phone')).json()
        self.assertIn({'name': 'object_1'}, result)
        self.assertNotIn({'name': 'object_2'}, result)
        self.assertIn({'name': 'object_mixed'}, result)

    def test_request_with_email(self) -> None:
        """Test values in response with specified email."""
        result = self.client.post(self.urls.get('get_form_by_email')).json()
        self.assertIn({'name': 'object_1'}, result)
        self.assertNotIn({'name': 'object_2'}, result)
        self.assertNotIn({'name': 'object_mixed'}, result)

    def test_request_with_date(self) -> None:
        """Test values in response with specified date."""
        result = self.client.post(self.urls.get('get_form_by_date')).json()
        self.assertIn({'name': 'object_1'}, result)
        self.assertNotIn({'name': 'object_2'}, result)
        self.assertNotIn({'name': 'object_mixed'}, result)

    def test_request_with_dash_date(self) -> None:
        """Test values in response with specified date with dashes."""
        result = self.client.post(
            self.urls.get('get_form_by_dash_date'),
        ).json()
        self.assertIn({'name': 'object_1'}, result)
        self.assertNotIn({'name': 'object_2'}, result)
        self.assertNotIn({'name': 'object_mixed'}, result)

    def test_request_with_text(self) -> None:
        """Test values in response with specified text."""
        result = self.client.post(self.urls.get('get_form_by_text')).json()
        self.assertIn({'name': 'object_1'}, result)
        self.assertNotIn({'name': 'object_2'}, result)
        self.assertNotIn({'name': 'object_mixed'}, result)

    def test_request_with_unique_together(self) -> None:
        """Test values in response with specified unique together fields."""
        result = self.client.post(
            self.urls.get('get_form_by_unique_together'),
        ).json()
        self.assertIn({'name': 'object_1'}, result)
        self.assertNotIn({'name': 'object_2'}, result)
        self.assertNotIn({'name': 'object_mixed'}, result)

    def test_request_with_all_fields(self) -> None:
        """Test values in response with specified all fields."""
        result = self.client.post(
            self.urls.get('get_form_by_all'),
        ).json()
        self.assertIn({'name': 'object_1'}, result)
        self.assertNotIn({'name': 'object_2'}, result)
        self.assertNotIn({'name': 'object_mixed'}, result)

    @classmethod
    def tearDownClass(cls) -> None:
        """Detete test database."""
        cls.test_database.remove(Query().name == 'ABCDEF')
        cls.test_database.remove(Query().name == 'XYZ')
