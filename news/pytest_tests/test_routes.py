from http import HTTPStatus
from pytest_django.asserts import assertRedirects

from django.urls import reverse
import pytest


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id_for_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None)
    ),
)
def test_pages_availability(client, name, args, db, news):
    urls = reverse(name, args=args)
    response = client.get(urls)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_comment_client'), HTTPStatus.OK)
    )
)
@pytest.mark.parametrize(
    'name',
    (
        ('news:edit'),
        ('news:delete')
    )
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client,
    expected_status,
    name,
    id_comment_for_args
):
    url = reverse(name, args=id_comment_for_args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (
        ('news:edit'),
        ('news:delete')
    )
)
def test_redirect_for_anonymous_client(client, id_comment_for_args, name):
    login_url = reverse('users:login')
    url = reverse(name, args=id_comment_for_args)
    exepted_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, exepted_url)
