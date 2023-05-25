from django.contrib.auth.models import User, Group
from gardenspace.models import Plant, MyPlant, Location, LocationMyPlant
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


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
        fields = ['url', 'common_name', 'scientific_name', 'germination_temperature', 'requires_stratification', 'optimum_low_temp', 'optimum_high_temp', 'created_on', 'updated_on']


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
        read_only_fields = ['created_on', 'updated_on']


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    '''
    A way to retrieve the user without requiring the API client to provide user info in form data
    https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Location
        ordering = ['-id']
        fields = ['url', 'name', 'square_footage', 'active', 'user']
        read_only_fields = ['my_plants', 'created_on', 'updated_on']

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


class LocationMyPlantSerializer(serializers.HyperlinkedModelSerializer):
    '''
    A way to retrieve the user without requiring the API client to provide user info in form data
    https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    location = serializers.HyperlinkedRelatedField(view_name='location-detail', queryset=Location.objects.filter(active=True))
    my_plant = serializers.HyperlinkedRelatedField(view_name='myplant-detail', queryset=MyPlant.objects.all())

    class Meta:
        model = LocationMyPlant
        ordering = ['-id']
        fields = ['my_plant', 'location', 'user', 'active']
        read_only_fields = ['created_on', 'updated_on']
    
    def validate_user_matches(self, attrs):
        if not (attrs.get('my_plant').user == attrs.get('location').user == attrs.get('user')):
            raise serializers.ValidationError('both my_plant and location needs to be associated with current user')

    def validate(self, attrs):
        self.validate_user_matches(attrs)
        del(attrs['user'])
        return attrs
