from django.test import TestCase
from rest_framework.test import APIClient
from gardenspace.models import Plant, MyPlant, User, Location, LocationMyPlant


class LocationsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user1', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_locations_only_returns_for_user(self):
        location_1 = Location.objects.create(user=self.user, name='raised bed 1')
        user_2 = User.objects.create(username='user2', password='pass2')
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

    def test_post_locations_duplicate_name_for_different_users_should_succeed(self):
        user_2 = User.objects.create(username='user2', password='pass2')
        location_1 = Location.objects.create(user=user_2, name='raised bed 1')
        body = {
            'name': location_1.name
        }
        response = self.client.post('/locations/', body)
        self.assertEqual(response.status_code, 201, "error: {}".format(response.data))


    def test_put_locations_success(self):
        location_1 = Location.objects.create(user=self.user, name='raised bed 1')
        body = {
            'name': 'revised raised bed'
        }
        response = self.client.put("/locations/{}/".format(location_1.id), body)
        self.assertEqual(response.status_code, 200, "error: {}".format(response.data))

    def test_put_locations_only_allowed_for_user_owned_locations(self):
        user_2 = User.objects.create(username='user2', password='pass2')
        location_2 = Location.objects.create(user=user_2, name='raised bed 1')
        body = {
            'name': 'revised raised bed'
        }
        response = self.client.put("/locations/{}/".format(location_2.id), body)
        self.assertEqual(response.status_code, 404, "error: {}".format(response.data))

    def test_get_locations_should_only_return_active(self):
        location_1 = Location.objects.create(user=self.user, name='raised bed 1', active=True)
        location_2 = Location.objects.create(user=self.user, name='raised bed 2', active=False)
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, 200, "error: {}".format(response.data))
        self.assertEqual(response.data['count'], 1, "response should only include active locations")

