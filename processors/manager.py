from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from pandas import DataFrame

from processors.domain import (
    File,
    TransactionFrame,
    Transaction,
    PaginatorDomain,
    TransactionList,
)
from processors.repository import ProcessorDBInterface


@dataclass
class FileInput:
    """
    File Input Boundaries Of Manager
    """

    name: str
    file_data_frame: DataFrame
    user_id: int


@dataclass
class ListerHelper:
    """
    Helper to handle pagination, ordering and filtering
    """

    page: int
    limit: int
    order_by: str
    search: str


@dataclass
class Paginator:
    count: int
    page: int
    next_page: int


@dataclass
class TransactionsOut(Paginator):
    transactions: List[Transaction]


class ProcessorManagerInterface(ABC):
    """
    Interface to handle access to db
    """

    @abstractmethod
    def process_file(self, file_input: FileInput) -> bool:
        pass

    @abstractmethod
    def list_transactions(self, lister: ListerHelper, user_id: str) -> TransactionsOut:
        pass


class ProcessorManager(ProcessorManagerInterface):
    def __init__(self, repo_db: ProcessorDBInterface):
        self.repository: ProcessorDBInterface = repo_db

    def process_file(self, file_input: FileInput) -> bool:
        file = self.repository.create_file(
            File(filename=file_input.name, user_id=file_input.user_id)
        )
        return self.repository.create_transactions(
            TransactionFrame(file_input.file_data_frame), file.id, file_input.user_id
        )

    def list_transactions(self, lister: ListerHelper, user_id: int) -> TransactionsOut:
        result: TransactionList = self.repository.get_transactions_by_user_id(
            PaginatorDomain(**lister.__dict__), user_id
        )
        return TransactionsOut(
            count=result.count,
            page=result.page,
            next_page=result.next_page,
            transactions=result.transactions,
        )
