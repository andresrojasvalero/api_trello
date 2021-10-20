from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class BoardsTestCase(APITestCase):

  BASE_URL = 'http://127.0.0.1:8000'

  BOARD_DATA_TEST = {
    'name': 'TestBoard',
    'description': 'this board is only a test',
    'visibility': 'public',
  }

  BOARD_WRONG_DATA_TEST = {
    'descripton': 'this board is only a test',
    'visibility': 'public',
  }

  def setUp(self) -> None:
    user = User.objects.create_user(username='boardsTest', password='password')
    user_two = User.objects.create_user(username='boardsTestTwo', password='password')

    auth_response = self.client.post(f'{self.BASE_URL}/api/token/', data={'username': 'boardsTest', 'password': 'password'})
    token = auth_response.data.get('access')

    self.assertEqual(auth_response.status_code, 200)
    self.assertIsNotNone(token)

    auth_response_two = self.client.post(f'{self.BASE_URL}/api/token/', data={'username': 'boardsTestTwo', 'password': 'password'})
    token_two = auth_response_two.data.get('access')

    self.assertEqual(auth_response_two.status_code, 200)
    self.assertIsNotNone(token_two)

    self.user = user
    self.user_two = user_two
    self.token = f'Bearer {token}'
    self.token_two = f'Bearer {token_two}'

    create_response = self.client.post(
      f'{self.BASE_URL}/boards/',
      data=self.BOARD_DATA_TEST,
      HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    self.assertEqual(create_response.status_code, 201)

    self.board_id = create_response.data.get('id')

  # Post tests

  def test_create_board_without_auth(self):
    create_response = self.client.post(
      f'{self.BASE_URL}/boards/',
      data=self.BOARD_DATA_TEST
    )

    self.assertEqual(create_response.status_code, 401)

  def test_create_correctly(self):
    create_response = self.client.post(
      f'{self.BASE_URL}/boards/',
      data=self.BOARD_DATA_TEST,
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(create_response.status_code, 201)

  def test_create_with_wrong_data(self):
    create_response = self.client.post(
      f'{self.BASE_URL}/boards/',
      data=self.BOARD_WRONG_DATA_TEST,
      HTTP_AUTHORIZATION=self.token
    )
    
    self.assertEqual(create_response.status_code, 400)

  # Get tests

  def test_get_without_token(self):
    get_response = self.client.get(
      f'{self.BASE_URL}/boards/'
    )

    self.assertEqual(get_response.status_code, 401)


  def test_get_retrive(self):
    get_response = self.client.get(
      f'{self.BASE_URL}/boards/{self.board_id}/',
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(get_response.status_code, 200)

  def test_get_alien_retrive(self):
    get_response = self.client.get(
      f'{self.BASE_URL}/boards/Test{self.board_id}/',
      HTTP_AUTHORIZATION=self.token
    )

    isTrue = False
    if get_response.status_code in [404, 401]:
      isTrue = True

    self.assertTrue(isTrue)

  # Update tests

  def test_update_whitout_permissions(self):
    update_response = self.client.patch(
      f'{self.BASE_URL}/boards/{self.board_id}/',
      data={
        'name': 'visibility'
      },
    )

    self.assertEqual(update_response.status_code, 401)

  def test_update(self):
    update_response = self.client.patch(
      f'{self.BASE_URL}/boards/{self.board_id}/',
      data={
        'name': 'visibility'
      },
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(update_response.status_code, 200)

  def test_update_board_other_user (self):
    update_response = self.client.patch(
      f'{self.BASE_URL}/boards/{self.board_id}00/',
      data={
        'name': 'visibility'
      },
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(update_response.status_code, 404)

  # Delete tests

  def test_delete_without_permissions(self):
    delete_response = self.client.delete(f'{self.BASE_URL}/boards/{self.board_id}/')

    self.assertEqual(delete_response.status_code, 401)

  def test_delete(self):
    delete_response = self.client.delete(f'{self.BASE_URL}/boards/{self.board_id}/', HTTP_AUTHORIZATION=self.token)

    self.assertEqual(delete_response.status_code, 204)

  def test_delete_board_other_user(self):
    delete_response = self.client.delete(f'{self.BASE_URL}/boards/{self.board_id}00/', HTTP_AUTHORIZATION=self.token)

    self.assertEqual(delete_response.status_code, 404)

  # Action Members tests
  
  # Action Members post

  def test_action_members_post_without_permissios(self):
    add_response = self.client.post(
      f'{self.BASE_URL}/boards/{self.board_id}/members/',
      data={
        'id': self.user_two.id
      }
    )
  
    self.assertEqual(add_response.status_code, 401)

  def test_action_members_post(self):
    add_response = self.client.post(
      f'{self.BASE_URL}/boards/{self.board_id}/members/',
      data={
        'id': self.user_two.id
      },
      HTTP_AUTHORIZATION=self.token
    )
  
    self.assertEqual(add_response.status_code, 201)

  def test_action_members_post_wrong_data(self):
    add_response = self.client.post(
      f'{self.BASE_URL}/boards/{self.board_id}/members/',
      data={
        'other': 'test'
      },
      HTTP_AUTHORIZATION=self.token
    )
  
    self.assertEqual(add_response.status_code, 400)  

  def test_action_members_post_add_wrong_permissions(self):
    add_response = self.client.post(
      f'{self.BASE_URL}/boards/{self.board_id}/members/',
      data={
        'id': self.user.id
      },
      HTTP_AUTHORIZATION=self.token_two
    )
  
    self.assertEqual(add_response.status_code, 404)

  # Action Members delete

  def test_action_members_delete(self):
    add_response = self.client.post(
      f'{self.BASE_URL}/boards/{self.board_id}/members/',
      data={
        'id': self.user_two.id
      },
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(add_response.status_code, 201)

    remove_response = self.client.delete(
      f'{self.BASE_URL}/boards/{self.board_id}/members/',
      data={
        'id': self.user_two.id
      },
      HTTP_AUTHORIZATION=self.token
    )
  
    self.assertEqual(remove_response.status_code, 200)

  # Action Favorites tests

  def test_action_favorite_post(self):
    add_response = self.client.post(
      f'{self.BASE_URL}/boards/{self.board_id}/favorites/',
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(add_response.status_code, 201)

  def test_action_favorite_delete(self):
    add_response = self.client.post(
      f'{self.BASE_URL}/boards/{self.board_id}/favorites/',
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(add_response.status_code, 201)

    remove_response = self.client.delete(
      f'{self.BASE_URL}/boards/{self.board_id}/favorites/',
      HTTP_AUTHORIZATION=self.token
    )

    self.assertEqual(remove_response.status_code, 200)