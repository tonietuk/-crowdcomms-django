from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from foxes.models import Fox
from foxes.permissions import IsAFox
from rest_framework.response import Response
from bunnies.models import Bunny, RabbitHole
from foxes.serializers import NearbyRabbitHoleSerializer
import haversine as hs

# Create your views here.

@api_view(["GET"])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated & IsAFox])
def get_nearby_active_rabbit_holes(request):
    """
    As a fox, I want to be able to sniff out nearby populated rabbit holes
    Given my current latitude / longitude, return the location name + position + distance of the closest rabbit hole
    that contains at least one rabbit for my dinner, as a lat / lng pair
    """


    rabbit_holes = RabbitHole.objects.filter(bunnies__isnull=False)

    if not rabbit_holes:
        return Response({
                'message': 'Sorry, no bunny to be sniffed out!'
            }, status=404)
    
    
     
    fox_location = (request.user.fox.latitude, request.user.fox.longitude)
    closest_hole = rabbit_holes[0]
    closest_distance = _calculate_distance(fox_location, (rabbit_holes[0].latitude, rabbit_holes[0].longitude))
    
    for hole in rabbit_holes:
        new_distance = _calculate_distance(fox_location, (hole.latitude, hole.longitude))
        if new_distance < closest_distance:
            closest_hole = hole
            closest_distance = new_distance
    

    ser = NearbyRabbitHoleSerializer(
        instance={
            "location": closest_hole.location,
            "distance_km": closest_distance,
            "compass_direction": "N"
        }
    )
    
    return Response(data=ser.data)


def _calculate_distance(location1, location2):
    """
    Calculates the distance between two geolocation
    location1: tuple of (latitude, longitude)  as floats  of first coordinate
    location2: tuple of (latitude, longitude)  as floats  of second coordinate
    """
    return hs.haversine(location1,location2)
