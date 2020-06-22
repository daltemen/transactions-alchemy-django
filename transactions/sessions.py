from sqlalchemy.orm import sessionmaker

from transactions.settings import engine

DBSession = sessionmaker(bind=engine)

