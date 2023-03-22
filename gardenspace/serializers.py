from django.contrib.auth.models import User, Group
from gardenspace.models import Plant, MyPlant, Location
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plant
        ordering = ['-common_name']
        fields = ['url', 'common_name', 'scientific_name', 'germination_temperature', 'requires_stratification', 'optimum_low_temp', 'optimum_high_temp']

class MyPlantSerializer(serializers.HyperlinkedModelSerializer):
    plant = serializers.HyperlinkedRelatedField(view_name='plant-detail', queryset=Plant.objects.all())
    '''
    A way to retrieve the user without requiring the API client to provide user info in form data
    https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MyPlant
        ordering = ['-id']
        fields = ['url', 'plant', 'user', 'state']

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    '''
    A way to retrieve the user without requiring the API client to provide user info in form data
    https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Location
        ordering = ['-id']
        fields = ['url', 'name', 'square_footage', 'active', 'my_plants', 'user']
        read_only_fields = ['my_plants']

    def validate_location_name_is_unique_for_user(self, attrs):
        user = attrs.get('user')
        try:
            location = Location.objects.filter(user=user.id).filter(name=attrs.get('name'))
        except:
            return
        if location:
            raise serializers.ValidationError('user already has a location with this name')

    def validate(self, attrs):
        self.validate_location_name_is_unique_for_user(attrs)
        return attrs