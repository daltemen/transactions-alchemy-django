import datetime
from dataclasses import dataclass
from typing import Optional

from pandas import DataFrame


@dataclass
class TransactionFrame:
    """
    Transaction class for domain objects
    """
    data_frame: DataFrame


@dataclass
class File:
    """
    File class for domain objects
    """
    filename: str
    user_id: int
    id: Optional[str] = None
    created_at: Optional[datetime.date] = None
