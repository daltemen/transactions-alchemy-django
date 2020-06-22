import datetime
import uuid
from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import Session

from processors.domain import TransactionFrame, File
from processors.models import FileDB
from transactions.sessions import DBSession
from transactions.settings import engine


class ProcessorDBInterface(ABC):
    """
    Interface to handle access to db
    """

    @abstractmethod
    def create_file(self, file: File) -> File:
        pass

    @abstractmethod
    def create_transactions(
        self, transaction: TransactionFrame, file_id: str, user_id: int
    ) -> bool:
        pass

    @abstractmethod
    def get_transactions_by_user_id(self, user_id: str) -> List[TransactionFrame]:
        pass


class ProcessorDB(ProcessorDBInterface):
    def create_file(self, file: File) -> File:
        session: Session = DBSession()

        db_file: FileDB = FileDB(
            id=str(uuid.uuid4()),
            filename=file.filename,
            created_at=datetime.datetime.now().date(),
            user_id=file.user_id,
        )
        session.add(db_file)
        session.commit()

        file.id = db_file.id
        file.created_at = db_file.created_at
        return file

    def create_transactions(
        self, transaction: TransactionFrame, file_id: str, user_id: int
    ) -> bool:
        self._prepare_data_frame(transaction, file_id, user_id)

        transaction.data_frame.to_sql(
            "transactions",
            engine,
            if_exists="append",
            index_label="id"
        )
        return True

    @staticmethod
    def _prepare_data_frame(transaction: TransactionFrame, file_id: str, user_id: int):
        num_rows = transaction.data_frame.shape[0]

        uuid_list = [str(uuid.uuid4()) for _ in range(num_rows)]
        transaction.data_frame.insert(0, "id", uuid_list)

        user_id_list = [user_id] * num_rows
        file_id_list = [file_id] * num_rows

        transaction.data_frame["user_id"] = user_id_list
        transaction.data_frame["file_id"] = file_id_list

        transaction.data_frame.set_index("id", inplace=True)

    def get_transactions_by_user_id(self, user_id: str) -> List[TransactionFrame]:
        pass
