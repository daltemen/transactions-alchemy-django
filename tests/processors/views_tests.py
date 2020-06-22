import io
import unittest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.test import APIRequestFactory, force_authenticate

from processors.domain import Transaction
from processors.manager import TransactionsOut
from processors.views import TransactionsList, FileUploadView


class TransactionsListTest(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    @patch("processors.manager.ProcessorManager.list_transactions")
    @patch("processors.repository.ProcessorDB")
    def test_get(self, ProcessorDB, list_transactions):
        transactions = [
            Transaction(
                id="1",
                transaction_id="1",
                transaction_date="2020-01-10",
                transaction_amount=1000,
                client_id=1,
                client_name="name",
                file_id="1",
                user_id=1,
            )
        ]
        mock = TransactionsOut(count=10, page=1, next_page=2, transactions=transactions)
        list_transactions.return_value = mock
        view = TransactionsList.as_view()
        request = self.factory.get(
            "/v1/processors/transactions?limit=10&page=1&order_by=id&search=hello"
        )
        user = User()
        user.pk = 1
        force_authenticate(request, user=user)
        response = view(request)
        expected = {
            "count": 10,
            "page": 1,
            "next_page": 2,
            "transactions": [
                {
                    "id": "1",
                    "transaction_id": "1",
                    "transaction_date": "2020-01-10",
                    "transaction_amount": 1000,
                    "client_id": 1,
                    "client_name": "name",
                    "file_id": "1",
                    "user_id": 1,
                }
            ],
        }

        assert 200 == response.status_code
        assert expected == response.data


class FileUploadViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.file = (
            "transaction_id,transaction_date,transaction_amount,client_id,client_name "
            "52fba4fa-3a01-4961-a809-e343dd4f9597,2020-06-01,10000,1067,nombre cliente"
        ).encode()

    @patch("processors.manager.ProcessorManager.process_file")
    @patch("processors.repository.ProcessorDB")
    def test_post(self, ProcessorDB, process_file):
        process_file.return_value = True
        view = FileUploadView.as_view()
        csv = InMemoryUploadedFile(
            io.BytesIO(self.file), None, "test.csv", "text/csv", 1024, None
        )
        request = self.factory.post("/v1/processors/files", data={"file": csv})
        user = User()
        user.pk = 1
        force_authenticate(request, user=user)
        response = view(request)
        assert 204 == response.status_code
