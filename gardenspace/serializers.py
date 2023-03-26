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

    # def validate(self, attrs):
    #     import pdb 
    #     pdb.set_trace()

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

class LocationMyPlantSerializer(serializers.HyperlinkedModelSerializer):
    '''
    A way to retrieve the user without requiring the API client to provide user info in form data
    https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # location = serializers.HyperlinkedIdentityField(view_name='location-detail', lookup_field='id')
    location = serializers.HyperlinkedRelatedField(view_name='location-detail', queryset=Location.objects.all())
    my_plant = serializers.HyperlinkedRelatedField(view_name='myplant-detail', queryset=MyPlant.objects.all())
    # my_plant = NestedHyperlinkedRelatedField(view_name='location-my-plant-detail', parent_lookup_kwargs={'location_pk': 'location__pk'}, read_only=True)

    class Meta:
        model = LocationMyPlant
        ordering = ['-id']
        fields = ['my_plant', 'location','user']
    
    def validate(self, attrs):
        # import pdb 
        # pdb.set_trace()
        del(attrs['user'])
        return attrs
