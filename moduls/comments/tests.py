from django.contrib.auth.models import User
from moduls.comments.models import Comment
from moduls.boards.models import Board

# Create your tests here.
from moduls.lists.models import List
from django.test import TestCase
from rest_framework.test import APITestCase
from moduls.cards.models import Card

# Create your tests here.
class CommentsTestCase(APITestCase):
    def setUp(self) -> None:
        self.host = 'http://127.0.0.1:8000'
        user = User.objects.create_user(username='test2', password='test')
        response = self.client.post(f'{self.host}/api/token/', data={'username': 'test2', 'password': 'test'})
        self.token =response.data['access']
        """ self.user = User.objects.create(password= '123',
                                        is_superuser=False,
                                        username = 'user',
                                        first_name= 'user',
                                        email= 'user@gmail.com',
                                        is_staff= False,
                                        is_active=True,
                                        date_joined='2021-07-16T00:08:01.189958Z',
                                        last_name='user2') """

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
        
        self.comment = Comment.objects.create(message="crear vistas",
                                        card=self.card,
                                        owner=user)

    def test_get_comments(self):
        response = self.client.get(f'{self.host}/comments/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.data), 0)

    def test_create_comments(self):
        data = {
                "message": "hola", 
                "owner": 1,
                "card": 1
                }
        response = self.client.post(f'{self.host}/comments/', data= data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        total_comments = Comment.objects.all().count()
        self.assertNotEqual(total_comments, 0)

    def tests_patch_comments(self):
        data = {
            "message": "editado",
        }
        response = self.client.patch(f'{self.host}/comments/{self.comment.id}/', data= data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.message, data['message'])

    def test_delete_comments(self):
        response = self.client.delete(f'{self.host}/comments/{self.comment.id}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        total_self_especific_comments = Comment.objects.filter(id = self.comment.id).count()
        self.assertEqual(total_self_especific_comments, 0)
