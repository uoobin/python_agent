from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import viewsets
from api.models import FilterData
from api.serializer import FilterDataSerializer

import os
import pandas as pd
# Create your views here.
class FilterDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FilterData.objects.all()
    serializer_class = FilterDataSerializer

    def get(self, request):
        queryset = FilterData.objects.all()
        serializer = FilterDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = FilterDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            f = os.path.join(os.path.join(os.path.dirname(__file__),'../'), 'transaction_data.csv')
            df = pd.read_csv(f)
            df = df[df['timestamp'] == float(data['timestamp'])]
            for x, row in df.iterrows():
                if str(data['timestamp'])+'.csv' in os.listdir(os.path.join(os.path.dirname(__file__))):
                    with open(str(data['timestamp'])+'.csv','a') as fd:
                        fd.write(','.join([str(row['timestamp']), row['method'], row['url'], str(row['status_code']), str(row['latency']), str(row['cpu']), str(row['ram'])])+'\n')

                else:
                    with open(str(data['timestamp'])+'.csv', 'a') as fd:
                        fd.write('timestamp,method,url,status_code,latency,cpu,ram\n')
                        fd.write(','.join([str(row['timestamp']), row['method'], row['url'], str(row['status_code']), str(row['latency']), str(row['cpu']), str(row['ram'])])+'\n')
            return Response(serializer.data)
        return JsonResponse(serializer.errors, status=400)




# class FilterDataListAPI(APIView):
#     def get(self, request):
#         queryset = FilterData.objects.filter(timestamp__range=(1667463076,1667463107))
#         serializer = FilterDataSerializer(queryset, many=True)
#         return Response(serializer.data)
