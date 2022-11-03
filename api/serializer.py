from rest_framework import serializers
from middleware.models import SendData
from api.models import FilterData

class SendDataSerializer(serializers.ModelSerializer):
    class Meta :
        model = SendData
        fields = '__all__'

class FilterDataSerializer(serializers.ModelSerializer) :
    class Meta :
        model = FilterData
        fields = '__all__'