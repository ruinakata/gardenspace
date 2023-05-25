from django.test import TestCase
from gardenspace.serializers import LocationMyPlantSerializer
from collections import OrderedDict
from gardenspace.models import Plant, MyPlant, User, Location
from rest_framework import serializers

class LocationMyPlantSerializerUnitTest(TestCase):

	def setUp(self):
		self.user_1 = User.objects.create(username='user1', password='pass')
		self.user_2 = User.objects.create(username='user2', password='pass')
		self.plant_1 = Plant.objects.create(common_name='shiso', scientific_name='Perilla frutescens')
		self.serializer = LocationMyPlantSerializer()

	def test_validate_user_matches_location_user_mismatch_should_error(self):
		attrs = self.set_up_attrs(self.user_2, self.user_1, self.user_1)
		self.assertRaises(serializers.ValidationError, self.serializer.validate_user_matches, attrs)

	def test_validate_user_matches_my_plant_user_mismatch_should_error(self):
		attrs = self.set_up_attrs(self.user_1, self.user_2, self.user_1)
		self.assertRaises(serializers.ValidationError, self.serializer.validate_user_matches, attrs)

	def test_validate_user_matches_auth_user_mismatch_should_error(self):
		attrs = self.set_up_attrs(self.user_1, self.user_1, self.user_2)
		self.assertRaises(serializers.ValidationError, self.serializer.validate_user_matches, attrs)

	def set_up_attrs(self, location_user, my_plant_user, auth_user):
		location = Location.objects.create(user=location_user, name='raised bed 1')
		my_plant = MyPlant.objects.create(plant=self.plant_1, state='unplanted', user=my_plant_user)
		attrs = OrderedDict()
		attrs['my_plant'] = my_plant
		attrs['location'] = location
		attrs['user'] = auth_user
		return attrs