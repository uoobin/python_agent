from django.shortcuts import render

from rest_framework.response import Response
from middleware.models import SendData
from rest_framework.views import APIView
from api.serializer import SendDataSerializer
# Create your views here.
class SendDataListAPI(APIView):
    def get(self, request):
        queryset = SendData.objects.all()
        serializer = SendDataSerializer(queryset, many=True)
        return Response(serializer.data)