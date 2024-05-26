from http import HTTPStatus

# import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(
    client, news_id_for_args, form_comment_data
):
    url = reverse('news:detail', args=news_id_for_args)
    client.post(url, data=form_comment_data)
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_can_create_comment(
    author_comment_client,
    news_id_for_args,
    form_comment_data,
    news,
    author,
):
    url = reverse('news:detail', args=news_id_for_args)
    response = (
        author_comment_client.post(url, data=form_comment_data)
    )
    assertRedirects(response, f'{url}#comments')
    comment_count = Comment.objects.count()
    assert comment_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_comment_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(
    author_comment_client,
    news_id_for_args,
):
    url = reverse('news:detail', args=news_id_for_args)
    response = author_comment_client.post(
        url, data={'text': f'Some {BAD_WORDS[0]} text'}
    )
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comment_count = Comment.objects.count()
    assert comment_count == 0

# Реализация проверки удаления коммента для автор
# и не автора коммента. не знаю нормально ли сделать это в одной
# функции, поэтому просто закомментил ее. И оставил работу как по тз
# теории.

# @pytest.mark.parametrize(
#     'parametrized_client, exepted_count_comment',
#     (
#         (pytest.lazy_fixture('author_comment_client'), 0),
#         (pytest.lazy_fixture('reader_client'), 1),
#     )
# )
# def test_author_can_reader_cant_delete_comment(
#     parametrized_client,
#     id_comment_for_args,
#     news_id_for_args,
#     exepted_count_comment,
# ):
#     url = reverse('news:delete', args=id_comment_for_args)
#     url_news = reverse('news:detail', args=news_id_for_args)
#     url_to_comment = url_news + '#comments'
#     response = parametrized_client.delete(url)
#     if exepted_count_comment == 0:
#         assertRedirects(response, url_to_comment)
#     else:
#         response.status_code == HTTPStatus.NOT_FOUND
#     comment_count = Comment.objects.count()
#     assert comment_count == exepted_count_comment


def test_author_can_delete_comment(
    author_comment_client,
    id_comment_for_args,
    news_id_for_args,
):
    url_delete = reverse('news:delete', args=id_comment_for_args)
    url_news = reverse('news:detail', args=news_id_for_args)
    url_to_comment = url_news + '#comments'
    response = author_comment_client.delete(url_delete)
    assertRedirects(response, url_to_comment)
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_reader_cant_delete_comments_of_author_user(
    reader_client,
    id_comment_for_args,
):
    url_delete = reverse('news:delete', args=id_comment_for_args)
    response = reader_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_author_can_edit_comment(
    author_comment_client,
    form_comment_data,
    id_comment_for_args,
    news_id_for_args,
    comment
):
    url_news = reverse('news:detail', args=news_id_for_args)
    edit_url = reverse('news:edit', args=id_comment_for_args)
    url_to_comment = url_news + '#comments'
    response = author_comment_client.post(edit_url, data=form_comment_data)
    assertRedirects(response, url_to_comment)
    comment.refresh_from_db()
    assert comment.text == form_comment_data['text']


def test_user_cant_edit_comment_of_another_user(
    reader_client,
    form_comment_data,
    id_comment_for_args,
    comment
):
    comment_save_text = comment.text
    edit_url = reverse('news:edit', args=id_comment_for_args)
    respose = reader_client.post(edit_url, data=form_comment_data)
    assert respose.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_save_text


# @pytest.mark.parametrize(
#     'parametrized_client, exepted_status',
#     (
#         (pytest.lazy_fixture('author_comment_client'), None),
#         (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
#     )
# )
# def test_author_can_reader_cant_edit_comment(
#     parametrized_client,
#     exepted_status,
#     id_comment_for_args,
#     news_id_for_args,
#     form_comment_data,
#     comment,
# ):
#     save_comment_text = comment.text
#     url_news = reverse('news:detail', args=news_id_for_args)
#     edit_url = reverse('news:edit', args=id_comment_for_args)
#     url_to_comment = url_news + '#comments'
#     response = parametrized_client.post(edit_url, data=form_comment_data)
#     if exepted_status == HTTPStatus.NOT_FOUND:
#         assert response.status_code == exepted_status
#         comment.refresh_from_db()
#         assert comment.text == save_comment_text
#     else:
#         assertRedirects(response, url_to_comment)
#         comment.refresh_from_db()
#         assert comment.text == form_comment_data['text']
