import pytest
from datetime import datetime, timedelta

from django.test.client import Client

from news.models import News, Comment
from django.conf import settings


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='user')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='another')


@pytest.fixture
def author_comment_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(
        text='some text',
        title='some title'
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        text='some text for comment',
        news=news,
        author=author,
    )
    return comment


@pytest.fixture
def news_id_for_args(news):
    return (news.id,)


@pytest.fixture
def id_comment_for_args(comment):
    return (comment.id,)


@pytest.fixture
def create_news_list(db):
    """Create a list of news more than the maximum available on one page"""
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'news{index}',
            text='Some text',
            date=today - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return News.objects


@pytest.fixture
def create_some_comments(news, author):
    today = datetime.today()
    Comment.objects.bulk_create(
        Comment(
            text=f'Some text {index}',
            news=news,
            author=author,
            created=today + timedelta(days=index))
        for index in range(10)
    )
    return Comment.objects
