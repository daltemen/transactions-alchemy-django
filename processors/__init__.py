from processors.models import Base
from transactions.settings import engine

Base.metadata.create_all(engine)
