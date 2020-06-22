import pandas
from django.core.files.uploadedfile import InMemoryUploadedFile
from pandas import DataFrame
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from processors.manager import ProcessorManager, FileInput
from processors.repository import ProcessorDB


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        file: InMemoryUploadedFile = request.data.get("file")
        name = file.name
        result: DataFrame = pandas.read_csv(file)

        manager = ProcessorManager(ProcessorDB())
        file_input = FileInput(name=name, file_data_frame=result, user_id=request.user.id)
        success = manager.process_file(file_input)

        return Response(status=204)
