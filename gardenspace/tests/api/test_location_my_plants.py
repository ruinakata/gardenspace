from django.test import TestCase
from rest_framework.test import APIClient
from gardenspace.models import Plant, MyPlant, User, Location, LocationMyPlant
import json


class LocationMyPlantsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user1', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.plant_1 = Plant.objects.create(common_name='shiso', scientific_name='Perilla frutescens')
        self.my_plant_1 = MyPlant.objects.create(plant_id=self.plant_1.id, state='unplanted', user_id=self.user.id)
        self.location_1 = Location.objects.create(user=self.user, name='raised bed 1')

    def test_post_location_myplants_success(self):
        body = {
            "location": "/locations/{}/".format(self.location_1.id),
            "my_plant": "/my_plants/{}/".format(self.my_plant_1.id)
        }
        response = self.client.post("/location_my_plants/", body)
        self.assertEqual(response.status_code, 201, "error: {}".format(response.data))

    def test_post_location_myplants_should_error_when_user_mismatch(self):
        user_2 = User.objects.create(username='user2', password='pass2')
        user_2_location = Location.objects.create(user=user_2, name='veggie garden')
        body = {
            "location": "/locations/{}/".format(user_2_location.id),
            "my_plant": "/my_plants/{}/".format(self.my_plant_1.id)
        }
        response = self.client.post("/location_my_plants/", body)
        self.assertEqual(response.status_code, 400, "error: {}".format(response.data))

    def test_post_location_myplants_should_transplant_if_my_plant_already_planted(self):
        location_my_plant = LocationMyPlant.objects.create(location=self.location_1, my_plant=self.my_plant_1)
        location_2 = Location.objects.create(user=self.user, name='raised bed 2')
        body = {
            "location": "/locations/{}/".format(location_2.id),
            "my_plant": "/my_plants/{}/".format(self.my_plant_1.id)
        }
        response = self.client.post("/location_my_plants/", body)
        self.assertEqual(response.status_code, 201, "error: {}".format(response.data))
        locations_for_my_plant = LocationMyPlant.objects.filter(my_plant=self.my_plant_1).filter(active=True)
        self.assertEqual(locations_for_my_plant.count(), 1)

    def test_delete_location_myplants_success_should_inactivate_object(self):
        location_my_plant = LocationMyPlant.objects.create(location=self.location_1, my_plant=self.my_plant_1)
        response = self.client.delete("/location_my_plants/{}/".format(location_my_plant.id))
        self.assertEqual(response.status_code, 204, "error: {}".format(response.data))
        location_my_plant = LocationMyPlant.objects.filter(id=location_my_plant.id).get()
        self.assertEqual(location_my_plant.active, False, "location_my_plant should have been inactivated")

    def test_delete_location_myplants_fails_for_mismatched_user(self):
        user_2 = User.objects.create(username='user2', password='pass2')
        user_2_myplant = MyPlant.objects.create(plant_id=self.plant_1.id, state='unplanted', user_id=user_2.id)
        user_2_location = Location.objects.create(user=user_2, name='veggie garden')
        location_my_plant = LocationMyPlant.objects.create(location=user_2_location, my_plant=user_2_myplant)
        response = self.client.delete("/location_my_plants/{}/".format(location_my_plant.id))
        self.assertEqual(response.status_code, 404, "error: {}".format(response.data))

    def test_get_location_id_myplants_success(self):
        location_my_plant_1 = LocationMyPlant.objects.create(location=self.location_1, my_plant=self.my_plant_1)
        location_2 = Location.objects.create(user=self.user, name='raised bed 2')
        location_my_plant_2 = LocationMyPlant.objects.create(location=location_2, my_plant=self.my_plant_1)
        response = self.client.get("/locations/{}/my_plants/".format(self.location_1.id))
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(response.data['count'], 1)
        result = json.loads(response.content)
        self.assertEqual(result['results']['my_plant'], 'http://testserver/my_plants/5/')

    def test_get_location_id_myplants_only_returns_for_user(self):
        pass
