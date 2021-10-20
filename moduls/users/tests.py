from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserTestCase(APITestCase):

    BASE_URL = 'http://127.0.0.1:8000'

    USER_DATA_TEST = {
        'username': 'testUser',
        'password': 'password',
        'first_name' : 'User',
        'email' : 'user@gmail.com',
        'last_name' : 'lastname',
    }

    USER_WRONG_DATA_TEST = {
        'first_name' : 'User',
        'email' : 'user@gmail.com',
        'last_name' : 'lastname',
    }

    def setUp(self) -> None:

        user = User.objects.create_user( username='userTest', password='password')

        auth_response = self.client.post(
            f'{self.BASE_URL}/api/token/', 
            data={'username': 'userTest', 
            'password': 'password'}
        )

        token = auth_response.data.get('access')

        self.assertEqual(auth_response.status_code, 200)
        self.assertIsNotNone(token)

        self.user = user

        self.token = f'Bearer {token}'

    # Get tests

    def test_get_user(self):
        response = self.client.get(f'{self.BASE_URL}/users/')
        self.assertEqual(response.status_code, 401)


    def test_create_correctly(self):
        create_response = self.client.post(
            f'{self.BASE_URL}/users/',
            data=self.USER_DATA_TEST,
        )
        self.assertEqual(create_response.status_code, 201)

    def test_create_whit_wrong_data(self):
        create_response = self.client.post(
            f'{self.BASE_URL}/users/',
            data=self.USER_WRONG_DATA_TEST,
        )
        self.assertEqual(create_response.status_code, 400)

    # Token tests

    def test_get_token(self):

        auth_response = self.client.post(
            f'{self.BASE_URL}/api/token/', 
            data={'username': 'userTest', 
            'password': 'password'}
        )
        token = auth_response.data.get('access')

        self.assertEqual(auth_response.status_code, 200)
        self.assertIsNotNone(token)

    # Patch tests
    def test_update(self):
        update_response = self.client.patch(
        f'{self.BASE_URL}/users/{self.user.id}/',
        data={
            'username': 'visibility'
        },
        HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(update_response.status_code, 200)

