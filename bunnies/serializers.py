from rest_framework import serializers

from bunnies.models import Bunny, RabbitHole


class RabbitHoleSerializer(serializers.ModelSerializer):

    bunnies = serializers.PrimaryKeyRelatedField(many=True, queryset=Bunny.objects.all())
    bunny_count = serializers.SerializerMethodField()

    def get_bunny_count(self, obj):
        return Bunny.objects.filter(home=obj).count()

    class Meta:
        model = RabbitHole
        fields = ('location', 'bunnies', 'bunny_count', 'owner', 'latitude', 'longitude')


class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(queryset=RabbitHole.objects.all(), slug_field='location')
    family_members = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        return obj.home.bunnies.all().exclude(id=obj.id).values_list('name', flat=True)

    def validate(self, attrs):
        return attrs

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')

