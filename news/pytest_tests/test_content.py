import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

HOME_URL = reverse('news:home')


def test_news_count(client, create_news_list):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, create_news_list):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(
    client,
    create_some_comments,
    news_id_for_args
):
    response = client.get(reverse('news:detail', args=news_id_for_args))
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_time_stamps = [comment.created for comment in all_comments]
    sorted_time_stamps = sorted(all_time_stamps)
    assert all_time_stamps == sorted_time_stamps


@pytest.mark.parametrize(
    'parametrized_client, form_in_page',
    (
        (pytest.lazy_fixture('reader_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_form_has_for_different_users(
    news_id_for_args,
    parametrized_client,
    form_in_page,
):
    url = reverse('news:detail', args=news_id_for_args)
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_page
    if form_in_page:
        assert isinstance(response.context['form'], CommentForm)
