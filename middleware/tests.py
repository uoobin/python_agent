from nturl2path import url2pathname
from operator import methodcaller
from sqlite3 import Timestamp
from django.conf import settings
from django.db import connection
from django.template import Template, Context

from middleware.models import SendData
from api.models import FilterData

import os
import time
import csv
import psutil

class SimpleMiddleware(object):    
    def __init__(self, get_response):        
        self.get_response = get_response

    def makeFile(self, timestamp, method, url, status_code, latency, cpu, ram):
        if 'transaction_data.csv' in os.listdir(os.path.join(os.path.dirname(__file__), '../')):
            with open('transaction_data.csv','a') as fd:
                fd.write(','.join([str(timestamp), method, url, str(status_code), str(latency), str(cpu), str(ram)])+'\n')

        else:
            with open('transaction_data.csv', 'a') as fd:
                fd.write('timestamp,method,url,status_code,latency,cpu,ram\n')
                fd.write(','.join([str(timestamp), method, url, str(status_code), str(latency), str(cpu), str(ram)])+'\n')
    
    def __call__(self, request):

        start_time = time.time()

        response = self.get_response(request)

        timestamp = time.time()
        method = request.method
        url = request.path
        status_code = response.status_code
        latency = timestamp - start_time

        cpu = psutil.cpu_percent(5)
        ram = psutil.virtual_memory().used

        self.makeFile(timestamp, method, url, status_code, latency, cpu, ram)

        SendData(
            timestamp = timestamp,
            method = method,
            url = url,
            status_code = status_code,
            latency = latency,
            cpu = cpu,
            ram = ram
        ).save()

        return response