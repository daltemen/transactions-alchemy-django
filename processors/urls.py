from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from processors.views import FileUploadView

urlpatterns = [
    path('files', FileUploadView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
