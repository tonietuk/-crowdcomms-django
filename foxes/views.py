from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from foxes.permissions import IsAFox
from rest_framework.response import Response
from foxes.serializers import NearbyRabbitHoleSerializer

# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated & IsAFox])
def get_nearby_active_rabbit_holes(self):
    """
    As a fox, I want to be able to sniff out nearby populated rabbit holes
    Given my current latitude / longitude, return the location name + position + distance of the closest rabbit hole
    that contains at least one rabbit for my dinner, as a lat / lng pair
    """
    ser = NearbyRabbitHoleSerializer(
        instance={
            "location": "???",
            "distance_km": 0.0,
            "compass_direction": "N"
        }
    )
    return Response(data=ser.data)
