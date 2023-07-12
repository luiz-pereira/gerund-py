from django.shortcuts import render
from rest_framework import viewsets
from .serializers import OutgoingVariationsSerializer, OriginalOutgoingSerializer, IncomingVariationsSerializer, OriginalIncomingSerializer
from .models import OriginalOutgoing, OriginalIncoming, OutgoingVariations, IncomingVariations

# Create your views here.

class OutgoingVariationView(viewsets.ModelViewSet):
    serializer_class = OutgoingVariationsSerializer
    queryset = OutgoingVariations.objects.all()

class OriginalOutgoingView(viewsets.ModelViewSet):
    serializer_class = OriginalOutgoingSerializer
    queryset = OriginalOutgoing.objects.all()

class IncomingVariationView(viewsets.ModelViewSet):
    serializer_class = IncomingVariationsSerializer
    queryset = IncomingVariations.objects.all()

class OriginalIncomingView(viewsets.ModelViewSet):
    serializer_class = OriginalIncomingSerializer
    queryset = OriginalIncoming.objects.all()
