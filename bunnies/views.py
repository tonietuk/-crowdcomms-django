from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from bunnies.models import Bunny, RabbitHole
from bunnies.permissions import RabbitHolePermissions
from bunnies.serializers import BunnySerializer, RabbitHoleSerializer


class RabbitHoleViewSet(viewsets.ModelViewSet):
    serializer_class = RabbitHoleSerializer
    permission_classes = (IsAuthenticated, RabbitHolePermissions)
    queryset = RabbitHole.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        if self.request.user.is_superuser is False:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class BunnyViewSet(viewsets.ModelViewSet):
    serializer_class = BunnySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Bunny.objects.all()

    def create(self, request, *args, **kwargs):
        rabbit_hole = RabbitHole.objects.get(location=request.data['home'])
        if rabbit_hole.bunnies.count() >= rabbit_hole.bunnies_limit:
            return Response({
                'message': 'Bad request'
            }, status=400)

        return super().create(request, *args, **kwargs)