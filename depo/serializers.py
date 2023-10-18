from rest_framework.serializers import ModelSerializer
from depo import models


class OutgoingSerializer(ModelSerializer):
    class Meta:
        model = models.Outgoing
        fields = '__all__'


class IncomingSerializer(ModelSerializer):
    class Meta:
        model = models.Incoming
        fields = '__all__'


class IncomingDetailSerializer(ModelSerializer):
    class Meta:
        model = models.IncomingDetail
        fields = '__all__'


class DetailOutgoingSerializer(ModelSerializer):
    class Meta:
        model = models.DetailOutgoing
        fields = '__all__'
