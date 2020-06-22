from django.apps import AppConfig
from processors.models import Base
from transactions.settings import engine


class ProcessorsConfig(AppConfig):
    name = "processors"

    def ready(self):
        try:
            Base.metadata.create_all(engine)
        except Exception as e:
            print(e)
