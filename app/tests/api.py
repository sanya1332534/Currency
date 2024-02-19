from django.urls import reverse

from currency.models import Source, Rate


def test_get_rate_list(api_client_auth):
    response = api_client_auth.get(reverse('currency_api:rate-list'))
    assert response.status_code == 200
    assert response.json()


def test_post_rate_list_empty_body(api_client_auth):
    response = api_client_auth.post(reverse('currency_api:rate-list'))
    assert response.status_code == 400
    assert response.json() == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_post_rate_list_valid_data(api_client_auth):
    initial_count = Rate.objects.count()
    source = Source.objects.create(name='Test', code_name='test')
    payload = {
        'buy': '37.00',
        'sell': '38.00',
        'source': source.id
    }
    response = api_client_auth.post(reverse('currency_api:rate-list'), data=payload)
    assert response.status_code == 201
    assert Rate.objects.count() == initial_count + 1


def test_post_rate_list_invalid_data(api_client_auth):
    source = Source.objects.create(name='Test', code_name='test')
    payload = {
        'buy': '37.000',
        'sell': '38.00',
        'source': source.id,
    }
    response = api_client_auth.post(reverse('currency_api:rate-list'), data=payload)
    assert response.status_code == 400
    assert response.json() == {
        'buy': ['Ensure that there are no more than 2 decimal places.']
    }


def test_create_source_api(api_client_auth):
    data = {
        'name': 'Test Source',
        'code_name': 'test_source',
        'source_url': 'http://example.com'
    }
    response = api_client_auth.post(reverse('currency_api:source-list'), data, format='json')
    assert response.status_code == 201
    assert Source.objects.filter(code_name='test_source').exists()


def test_get_source_api(api_client):
    response = api_client.get(reverse('currency_api:source-list'))
    assert response.status_code == 200
    results = response.data['results']
    for item in results:
        assert 'source_url' in item
        assert 'name' in item
        assert 'code_name' in item


def test_update_source_api(api_client_auth, source):
    updated_data = {
        'name': 'Updated Name',
        'code_name': 'updated_source',
        'source_url': 'http://example_updated.com'
    }
    response = api_client_auth.put(
        reverse('currency_api:source-detail', kwargs={'pk': source.pk}),
        updated_data,
        format='json'
    )
    assert response.status_code == 200
    source.refresh_from_db()
    assert source.code_name == 'updated_source'


def test_delete_source_api(api_client_auth, source):
    response = api_client_auth.delete(reverse('currency_api:source-detail', kwargs={'pk': source.pk}))
    assert response.status_code == 204
    assert not Source.objects.filter(pk=source.pk).exists()
