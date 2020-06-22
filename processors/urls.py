from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from processors.views import FileUploadView, TransactionsList

urlpatterns = [
    path("files", FileUploadView.as_view()),
    path("transactions", TransactionsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
