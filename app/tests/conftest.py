import pytest
from django.core.management import call_command
from currency.models import Source


@pytest.fixture(autouse=True, scope="function")
def enable_db_access_for_all_tests(db):
    """
    give access to database for all tests
    """


@pytest.fixture()
def api_client():
    from rest_framework.test import APIClient
    client = APIClient()
    yield client


@pytest.fixture(scope='function')
def api_client_auth(django_user_model):
    from rest_framework.test import APIClient
    client = APIClient()

    email = 'email@example.com'
    password = 'superSecretPassword'
    phone = '380730414062'

    user = django_user_model(email=email, phone=phone)
    user.set_password(password)
    user.save()

    client.force_authenticate(user=user)

    yield client

    user.delete()


@pytest.fixture(scope='session', autouse=True)
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = (
            'sources.json',
            'rates.json'
        )

        for fixture in fixtures:
            call_command('loaddata', f'app/tests/fixtures/{fixture}')


@pytest.fixture
def source(db):
    source_instance = Source.objects.create(
        name="TestSource",
        code_name="test_source",
        source_url="https://example.com"
    )
    yield source_instance
    source_instance.delete()
