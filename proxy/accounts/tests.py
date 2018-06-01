from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from core.tests import SetUpUserMixin


class ObtainJSONWebTokenTest(SetUpUserMixin, APITestCase):
    """
    Tests for ObtainJSONWebToken
    """

    def test_post(self):
        """
        test for post request to api_token_auth
        :return: 200
        """

        data = {
            'username': 'user',
            'password': 'adminadmin'
        }
        response = self.client.post(reverse('api_token_auth'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
