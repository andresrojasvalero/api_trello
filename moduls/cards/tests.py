from moduls.boards.models import Board
from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
from moduls.lists.models import List
from django.http import response
from django.test import TestCase
from rest_framework.test import APITestCase
from moduls.cards.models import Card

# Create your tests here.
class CardTestCase(APITestCase):
    def setUp(self) -> None:
        self.host = 'http://127.0.0.1:8000'
        user = User.objects.create_user(username='test', password='test')
        response = self.client.post(f'{self.host}/api/token/', data={'username': 'test', 'password': 'test'})
        self.token =response.data['access']
        self.board = Board.objects.create(name = 'qe',
                                    description = 'we',
                                    visibility = 'sd',
                                    created_at="2021-07-16T00:08:01.189958Z")


        self.lists = List.objects.create(name="api trello",
                                        position=3,
                                        created_at="2021-07-16T00:08:01.189958Z",
                                        board= self.board)


        self.card = Card.objects.create(
                                        owner=user,
                                        name="crear vistas",
                                        description="crear vistas", 
                                        position=2,
                                        list=self.lists,
                                        finalization_at="2021-07-16T00:08:01.189958Z")

    def test_get_cards(self):
        response = self.client.get(f'{self.host}/cards/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.data), 0)

    def test_create_card(self):
        data = {
                "owner": 1,
                "name": "crear vistas",
                "description": "crear vistas", 
                "position": 2,
                "members": 1,
                "list": 1,
                "finalization_at":"2021-07-16T00:08:01.189958Z"
                }
        response = self.client.post(f'{self.host}/cards/', data= data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        total_clase = Card.objects.all().count()
        self.assertNotEqual(total_clase, 0)

    def tests_patch_card(self):
        data = {
            "name": "nombre editado",
        }
        response = self.client.patch(f'{self.host}/cards/{self.card.id}/', data= data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        self.card.refresh_from_db()
        self.assertEqual(self.card.name, data['name'])

    def test_delete_card(self):
        response = self.client.delete(f'{self.host}/cards/{self.card.id}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        total_self_especific_cards = Card.objects.filter(id = self.card.id).count()
        self.assertEqual(total_self_especific_cards, 0)
