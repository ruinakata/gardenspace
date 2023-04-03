from django.contrib.auth.models import User, Group
from gardenspace.models import Plant, MyPlant, Location, LocationMyPlant
from gardenspace.serializers import UserSerializer, GroupSerializer, PlantSerializer, MyPlantSerializer, LocationSerializer, LocationMyPlantSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import generics


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


class LocationMyPlantCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
	"""
	API endpoint that allows a my_plant to be added from a location.
	"""
	queryset = LocationMyPlant.objects.all()
	serializer_class = LocationMyPlantSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def perform_create(self, serializer):
		my_plant = serializer.validated_data['my_plant']
		location = serializer.validated_data['location']
		location_my_plant_duplicates = LocationMyPlant.objects.all().filter(my_plant=my_plant, location=location, active=True)
		if location_my_plant_duplicates.count() > 0:
			for location_my_plant in location_my_plant_duplicates:
				location_my_plant.active = False
				location_my_plant.save()
		serializer.save()


class LocationMyPlantDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
	"""
	API endpoint that allows a my_plant to be deleted from a location.
	"""
	queryset = LocationMyPlant.objects.all()
	serializer_class = LocationMyPlantSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get_queryset(self):
		queryset = LocationMyPlant.objects.all().filter(location__user_id=self.request.user.id)
		return queryset

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

	def perform_destroy(self, instance):
		instance.active = False
		instance.save()

