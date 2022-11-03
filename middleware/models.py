from django.db import models

# Create your models here.
class SendData(models.Model):
    timestamp = models.FloatField()
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=50)
    status_code = models.IntegerField()
    latency = models.FloatField()
    cpu = models.FloatField()
    ram = models.IntegerField()