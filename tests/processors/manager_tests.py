import unittest
from unittest.mock import Mock

import pandas as pd

from processors.domain import TransactionList, Transaction
from processors.manager import (
    ProcessorManager,
    FileInput,
    ListerHelper,
    TransactionsOut,
)


class ProcessorManagerTest(unittest.TestCase):
    def setUp(self):
        d = {"col1": [1, 2], "col2": [3, 4]}
        self.user_id = 1
        self.data_frame_example = pd.DataFrame(data=d)
        self.db_processor_mock: Mock = Mock()
        self.processor_manager = ProcessorManager(self.db_processor_mock)

    def test_process_file(self):
        file_input = FileInput(
            name="track.csv",
            file_data_frame=self.data_frame_example,
            user_id=self.user_id,
        )
        self.db_processor_mock.create_transactions.return_value = True
        result = self.processor_manager.process_file(file_input)
        self.db_processor_mock.create_transactions.assert_called_once()
        assert result is True

    def test_list_transactions(self):
        mocked = TransactionList(
            transactions=[
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
            ],
            count=10,
            page=1,
            next_page=2,
        )
        self.db_processor_mock.get_transactions_by_user_id.return_value = mocked
        lister_helper = ListerHelper(page=1, limit=10, order_by="id", search="")
        result = self.processor_manager.list_transactions(lister_helper, self.user_id)

        expected = TransactionsOut(
            count=mocked.count,
            page=mocked.page,
            next_page=mocked.next_page,
            transactions=mocked.transactions,
        )
        assert expected == result
