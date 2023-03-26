from django.db import models
from django.contrib.auth.models import User


class Plant(models.Model):
	common_name = models.CharField(max_length=50, blank=False, null=False)
	scientific_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
	germination_temperature = models.IntegerField(blank=True, null=True)
	requires_stratification = models.BooleanField(blank=True, default=False)
	optimum_low_temp = models.IntegerField(blank=True, null=True)
	optimum_high_temp = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.common_name

	class Meta:
		ordering = ['common_name']


class MyPlant(models.Model):
	STATES = (('unplanted', 'unplanted'), ('planted', 'planted')) 

	plant = models.ForeignKey(Plant, blank=False, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	state = models.CharField(max_length=20, blank=False, choices=STATES, default='unplanted')


class Location(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False)
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	square_footage = models.IntegerField(blank=True, null=True)
	active = models.BooleanField(default=True)
	# my_plants = models.ManyToManyField(MyPlant, related_name='locations', blank=True)

	def __str__(self):
		return self.name

class LocationMyPlant(models.Model):
	location = models.ForeignKey(Location, null=False, on_delete=models.CASCADE)
	my_plant = models.ForeignKey(MyPlant, null=False, on_delete=models.CASCADE)

	class Meta:
		ordering = ['id']
		# db_table = 'gardenspace_location_my_plants'