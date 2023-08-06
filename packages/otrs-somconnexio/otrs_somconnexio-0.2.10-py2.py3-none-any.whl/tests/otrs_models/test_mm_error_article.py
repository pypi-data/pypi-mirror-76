# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.mm_error_article import MMErrorArticle


class MMErrorArticleTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_call_with_account_error(self, MockArticle):

        fake_error = {
            "statusCode": "400",
            "message": "El documentType no es un valor válido: 2",
            "fields": "documentType"
        }
        expected_article_arguments = {
            "Subject": "Error desde Mas Móvil en la creació d'un/a Account",
            "Body": u"fields: documentType\nmessage: El documentType no es un valor válido: 2\nstatusCode: 400\n",
            "ContentType": "text/plain; charset=utf8",
        }

        MMErrorArticle(fake_error, "Account").call()
        MockArticle.assert_called_once_with(expected_article_arguments)

    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_call_with_order_item_error(self, MockArticle):

        fake_error = {
            "statusCode": "400",
            "message": "El campo id debe estar relleno.",
            "fields": "id"
        }
        expected_article_arguments = {
            "Subject": "Error desde Mas Móvil en la creació d'un/a OrderItem",
            "Body": u"fields: id\nmessage: El campo id debe estar relleno.\nmm_account_id: 12345S\nstatusCode: 400\n",
            "ContentType": "text/plain; charset=utf8",
        }

        MMErrorArticle(fake_error, "OrderItem", "12345S").call()
        MockArticle.assert_called_once_with(expected_article_arguments)
