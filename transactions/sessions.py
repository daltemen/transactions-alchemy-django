from sqlalchemy.orm import sessionmaker, Session

from transactions.settings import engine

DBSession = sessionmaker(bind=engine)
# session: Session = DBSession()
# session.add()
