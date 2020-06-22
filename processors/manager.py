from abc import ABC, abstractmethod
from dataclasses import dataclass

from pandas import DataFrame

from processors.domain import File, TransactionFrame
from processors.repository import ProcessorDBInterface


@dataclass
class FileInput:
    """
    File Input Boundaries Of Manager
    """

    name: str
    file_data_frame: DataFrame
    user_id: int


class ProcessorManagerInterface(ABC):
    """
    Interface to handle access to db
    """

    @abstractmethod
    def process_file(self, file_input: FileInput) -> bool:
        pass


class ProcessorManager(ProcessorManagerInterface):
    def __init__(self, repo_db: ProcessorDBInterface):
        self.repository: ProcessorDBInterface = repo_db

    def process_file(self, file_input: FileInput) -> bool:
        file = self.repository.create_file(File(filename=file_input.name, user_id=file_input.user_id))
        return self.repository.create_transactions(TransactionFrame(file_input.file_data_frame), file.id, file_input.user_id)
