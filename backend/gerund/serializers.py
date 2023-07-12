from rest_framework import serializers
from .models import OriginalOutgoing, OriginalIncoming, OutgoingVariations, IncomingVariations

class OutgoingVariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoingVariations
        fields = ('id', 'content', 'original_outgoing', 'speech_binary')

class OriginalOutgoingSerializer(serializers.ModelSerializer):
    outgoing_variation_set = OutgoingVariationsSerializer(many=True, read_only=True)
    class Meta:
        model = OriginalOutgoing
        fields = ('id', 'content', 'type', 'original_incoming')

class IncomingVariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingVariations
        fields = ('id', 'content', 'original_incoming', 'embedding')

class OriginalIncomingSerializer(serializers.ModelSerializer):
    incoming_variation_set = IncomingVariationsSerializer(many=True, read_only=True)
    class Meta:
        model = OriginalIncoming
        fields = ('id', 'content', 'type')
