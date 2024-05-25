import pytest

from django.test.client import Client

from news.models import News, Comment


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
