from django.test import TestCase
from rest_framework.test import APIClient
from gardenspace.models import Plant, MyPlant, User, Location


class MyPlantsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user1', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.plant_1 = Plant.objects.create(common_name='shiso', scientific_name='Perilla frutescens')
        self.plant_2 = Plant.objects.create(common_name='sugar snap pea', scientific_name='Pisum sativum')
        self.my_plant_1 = MyPlant.objects.create(plant_id=self.plant_1.id, state='unplanted', user_id=self.user.id)
        self.my_plant_2 = MyPlant.objects.create(plant_id=self.plant_1.id, state='unplanted', user_id=self.user.id)

    def test_get_locations_only_returns_for_user(self):
        user_2 = User.objects.create(username='user2', password='pass2')
        location_1 = Location.objects.create(user=self.user, name='raised bed 1')
        location_2 = Location.objects.create(user=user_2, name='flower garden')
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, 200, "error: {}".format(response.data))
        self.assertEqual(response.data['count'], 1, "response should only include the location associated to user")

    def test_post_locations_success(self):
        body = {
            'name': 'veggie garden'
        }
        response = self.client.post('/locations/', body)
        self.assertEqual(response.status_code, 201, "error: {}".format(response.data))
        pk_of_location = response.data['url'].split('/')[-2]
        location_created = Location.objects.get(pk=pk_of_location)
        self.assertEqual(location_created.user_id, self.user.id, "created location is not associated with the correct user")

    def test_post_locations_duplicate_name_for_user_should_fail(self):
        location_1 = Location.objects.create(user=self.user, name='raised bed 1')
        body = {
            'name': location_1.name
        }
        response = self.client.post('/locations/', body)
        self.assertEqual(response.status_code, 400, "error: {}".format(response.data))

    # def test_add_my_plant_to_location(self):
    #     location_1 = Location.objects.create(user=self.user, name='raised bed 1')
    #     body = {
    #         'my_plant': "/my_plants/{}".format(self.my_plant_1.id)
    #     }
    #     response = self.client.post("/locations/{}/my_plants/".format(location_1.id), body)
    #     # import pdb 
    #     # pdb.set_trace()
    #     self.assertEqual(response.status_code, 201, "error: {}".format(response.data))

