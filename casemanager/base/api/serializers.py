from rest_framework.serializers import ModelSerializer
from base.models import Investigation
from base.models import Message

class InvestigationSerializers(ModelSerializer):
    class Meta:
        model = Investigation
        fields = '__all__'

class MessageSerializers(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'