from logging import Filter
from django.contrib import admin
from middleware.models import SendData
from api.models import FilterData
# Register your models here.
admin.site.register(SendData)
admin.site.register(FilterData)