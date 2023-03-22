from django.contrib.auth.models import User, Group
from gardenspace.models import Plant, MyPlant, Location
from gardenspace.serializers import UserSerializer, GroupSerializer, PlantSerializer, MyPlantSerializer, LocationSerializer
from rest_framework import viewsets
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = [permissions.IsAuthenticated]


class PlantViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows plants to be viewed or edited.
	"""
	queryset = Plant.objects.all()
	serializer_class = PlantSerializer
	permission_classes = [permissions.IsAuthenticated]


class MyPlantViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows my_plants to be viewed or edited.
	"""
	queryset = MyPlant.objects.all()
	serializer_class = MyPlantSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		queryset = MyPlant.objects.all().filter(user_id=self.request.user.id).order_by('id')
		return queryset


class LocationViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows locations to be viewed or edited.
	"""
	queryset = Location.objects.all()
	serializer_class = LocationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		queryset = Location.objects.all().filter(user_id=self.request.user.id).order_by('id')
		return queryset
