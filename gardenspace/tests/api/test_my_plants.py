from django.test import TestCase
from rest_framework.test import APIClient
from gardenspace.models import Plant, MyPlant, User


class MyPlantsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user1', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.plant_1 = Plant.objects.create(common_name='shiso', scientific_name='Perilla frutescens')
        self.plant_2 = Plant.objects.create(common_name='sugar snap pea', scientific_name='Pisum sativum')

    def test_post_myplants_success(self):
        response = self.client.post('/my_plants/', {'plant': '/plants/{}/'.format(self.plant_1.id), 'state': 'unplanted'})
        self.assertEqual(response.status_code, 201, "error: {}".format(response.data))
        pk_of_my_plant = response.data['url'].split('/')[-2]
        my_plant_created = MyPlant.objects.get(pk=pk_of_my_plant)
        self.assertEqual(my_plant_created.user_id, self.user.id, "created my_plant is not associated with the correct user")

    def test_post_myplants_wrong_state_should_400(self):
        response = self.client.post('/my_plants/', {'plant': '/plants/{}/'.format(self.plant_1.id), 'state': 'dead'})
        self.assertEqual(response.status_code, 400, "error: {}".format(response.data))

    def test_get_myplants_only_returns_for_user(self):
        user_2 = User.objects.create(username='user2', password='pass2')
        my_plant_1 = MyPlant.objects.create(plant_id=self.plant_1.id, state='unplanted', user_id=self.user.id)
        my_plant_2 = MyPlant.objects.create(plant_id=self.plant_1.id, state='unplanted', user_id=user_2.id)
        response = self.client.get('/my_plants/')
        self.assertEqual(response.status_code, 200, "error: {}".format(response.data))
        self.assertEqual(response.data['count'], 1, "response should only include the my_plant associated to user")

    def test_get_my_plant_detail_success(self):
        my_plant_1 = MyPlant.objects.create(plant_id=self.plant_1.id, state='unplanted', user_id=self.user.id)
        response = self.client.get("/my_plants/{}/".format(my_plant_1.id))
        self.assertEqual(response.status_code, 200, "error: {}".format(response.data))



