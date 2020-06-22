import datetime
from dataclasses import dataclass
from typing import Optional, List

from pandas import DataFrame


@dataclass
class TransactionFrame:
    """
    Transaction class in Frame Repr for domain objects
    """

    data_frame: DataFrame


@dataclass
class Transaction:
    """
    Transaction class for domain objects used by get
    """

    id: str
    transaction_id: str
    transaction_date: str
    transaction_amount: int
    client_id: int
    client_name: str
    file_id: str
    user_id: int


@dataclass
class TransactionList:
    transactions: List[Transaction]
    count: int
    page: int
    next_page: int


@dataclass
class PaginatorDomain:
    page: int
    limit: int
    order_by: str
    search: str


@dataclass
class File:
    """
    File class for domain objects
    """

    filename: str
    user_id: int
    id: Optional[str] = None
    created_at: Optional[datetime.date] = None
