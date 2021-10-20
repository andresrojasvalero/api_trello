from rest_framework.test import APITestCase
from moduls.boards.models import Board
from django.contrib.auth.models import User


# Create your tests here.

class ListTestCase(APITestCase):

  BASE_URL = 'http://127.0.0.1:8000'

  BOARD_DATA_TEST = {
    'name': 'TestBoard',
    'description': 'this board is only a test',
    'visibility': 'public',
  }
  
  def setUp(self) -> None:
    user = User.objects.create_user(username='boardsTest', password='password')

    auth_response = self.client.post(f'{self.BASE_URL}/api/token/', data={'username': 'boardsTest', 'password': 'password'})
    token = auth_response.data.get('access')

    self.assertEqual(auth_response.status_code, 200)
    self.assertIsNotNone(token)

    self.user = user
    self.token = f'Bearer {token}'

    board = Board.objects.create(owner=user, name = 'TestBoard', description = 'this board is only a test', visibility= 'public')
    self.board_id = board.id
    

    create_list_response = self.client.post(
      f'{self.BASE_URL}/lists/',
      data={
        'name': 'list test',
        'board': self.board_id,
        'position': 1
      },
      HTTP_AUTHORIZATION=self.token
    )
 
    self.assertEqual(create_list_response.status_code, 201)
  # Create tests
     
  def test_create_list_without_credentials(self):
    create_response = self.client.post(
      f'{self.BASE_URL}/lists/',
      data={
        'name': 'list test',
        'board': self.board_id,
        'position': 1
      }
    )

    self.assertEqual(create_response.status_code, 401)

  def test_create_wrong_data(self):
    create_response = self.client.post(
      f'{self.BASE_URL}/lists/',
      data={
        'name': 'list test',
        'position': -1
      },
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(create_response.status_code, 400)

  def test_create(self):
    create_response = self.client.post(
      f'{self.BASE_URL}/lists/',
      data={
        'name': 'list test',
        'board': self.board_id,
        'position': 1
      },
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(create_response.status_code, 201)

  # Get test

  def test_get_withou_credentials(self):
    get_response = self.client.get(f'{self.BASE_URL}/lists/')

    self.assertEqual(get_response.status_code, 401)

  def test_get(self):
    get_response = self.client.get(f'{self.BASE_URL}/lists/', HTTP_AUTHORIZATION=self.token)

    self.assertEqual(get_response.status_code, 200)

  # Update test

  def test_update_without_credentials(self):
    create_response = self.client.put(
      f'{self.BASE_URL}/lists/',
      data={
        'name': 'list test',
        'board': self.board_id,
        'position': 1
      }
    )

    self.assertEqual(create_response.status_code, 401)

  def test_update_wrong_data(self):
    create_response = self.client.patch(
      f'{self.BASE_URL}/lists/1/',
      data={
        'position': -1
      },
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(create_response.status_code, 400)

  def test_update(self):
    create_response = self.client.patch(
      f'{self.BASE_URL}/lists/1/',
      data={
        'name': 'testupdate'
      },
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(create_response.status_code, 200)

  # Delete tests

  def test_delete_without_credentials(self):
    delete_response = self.client.delete(f'{self.BASE_URL}/lists/1/')

    self.assertEqual(delete_response.status_code, 401)

  def test_delete_wrong_id(self):
    delete_response = self.client.delete(f'{self.BASE_URL}/lists/1abc/', HTTP_AUTHORIZATION=self.token)

    self.assertEqual(delete_response.status_code, 404)

  def test_delete(self):
    delete_response = self.client.delete(f'{self.BASE_URL}/lists/1/', HTTP_AUTHORIZATION=self.token)

    self.assertEqual(delete_response.status_code, 204)

  # Test Action Cards Get

  def test_action_get_cards_without_credentials(self):
    delete_response = self.client.get(
      f'{self.BASE_URL}/lists/1/cards/', 
      data={
        'board': self.board_id
      }
    )

    self.assertEqual(delete_response.status_code, 401)

  def test_action_get_cards_wituout_data(self):
    delete_response = self.client.get(
      f'{self.BASE_URL}/lists/1/cards/', 
      HTTP_AUTHORIZATION=self.token
    )
  
    self.assertEqual(delete_response.status_code, 400)
    
  
  def test_action_get_cards_wrong_data(self):
    delete_response = self.client.get(
      f'{self.BASE_URL}/lists/1/cards/', 
      data={
        'board': 12
      }, 
      HTTP_AUTHORIZATION=self.token
    )
    self.assertEqual(delete_response.status_code, 404)

  def test_action_get_cards(self):
    get_response = self.client.get(
      f'{self.BASE_URL}/lists/1/cards/', 
      data = {
        'board': self.board_id
      },
      HTTP_AUTHORIZATION=self.token,
    )

    self.assertEqual(get_response.status_code, 200)

  # Test Order Action Put
  
  def test_action_order_lists(self):
    get_response = self.client.put(
      f'{self.BASE_URL}/lists/1/order/', 
      data = {
        'board': self.board_id,
        'order': 2
      },
      HTTP_AUTHORIZATION=self.token,
    )

    self.assertEqual(get_response.status_code, 200)