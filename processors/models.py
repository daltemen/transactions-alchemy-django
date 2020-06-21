from sqlalchemy import Column, String, Date, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id: Column = Column(String(36), primary_key=True)
    transaction_id: Column = Column(String(36))
    transaction_date: Column = Column(Date)
    transaction_amount: Column = Column(Date)
    client_id: Column = Column(Numeric)  # UserId in system
    client_name: Column = Column(Numeric)

    file_id: Column = Column(String(36))

    def __repr__(self):
        return (
            f"<Transaction("
            f"id='{self.id}', "
            f"transaction_id='{self.transaction_id}', "
            f"transaction_date={self.transaction_date}, "
            f"transaction_amount={self.transaction_amount}"
            f"client_id={self.client_id}"
            f"client_id={self.client_name}"
            f")>"
        )


class File(Base):
    __tablename__ = "files"

    id: Column = Column(String(36), primary_key=True)
    filename: Column = Column(Text)
    created_at: Column = Column(Date)
    user_id: Column = Column(Numeric)

    def __repr__(self):
        return (
            f"<File("
            f"id='{self.id}', "
            f"filename='{self.filename}', "
            f"created_at={self.created_at}, "
            f"user_id={self.user_id}"
            f")>"
        )
