import json
from django.urls import reverse
from django.contrib.auth.models import User
import unittest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class BaseViewTest(APITestCase):
    client = APIClient()


    def login_a_user(self, username="", password=""):
        url = reverse(
            "token-auth"
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse("token-auth"),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def register_a_user(self, username="", password="", email=""):
        return self.client.post(
            reverse(
                "users:create_user",

            ),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email
                }
            ),
            content_type='application/json'
        )


    def setUp(self):

        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
        )

        self.data = {
            'username': self.user.username,
            'password': self.user.password
        }




class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_login_json_missing_fields(self):
        """
        Ensure JWT login view using JSON POST fails if missing fields.
        """
        response = self.login_a_user("test_user")

        self.assertEqual(response.status_code, 400)




class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """
    def test_register_a_user(self):
        response = self.register_a_user("new_user", "new_pass", "new_user@mail.com")
        # assert status code is 201 CREATED
        self.assertEqual(response.data["username"], "new_user")
        self.assertEqual(response.data["email"], "new_user@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.register_a_user()
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """

        response = self.register_a_user("user_1", "new_pass_1", "new_user_1@mail.com")

        self.assertEqual(201, response.status_code)

        response = self.register_a_user("user_1", "new_pass_2", "new_user_2@mail.com")

        self.assertEqual(400, response.status_code)


class TokenTestCase(BaseViewTest):
    """
    Handlers for getting tokens from the API, or creating arbitrary ones.
    """

    def setUp(self):
        super(TokenTestCase, self).setUp()

    def get_token(self, username="", password=""):
        response = self.login_a_user(username, password)
        return response.data['token']


class VerifyJSONWebTokenTestsSymmetric(TokenTestCase):

    def test_verify_jwt(self):
        """
        Test that a valid, non-expired token will return a 200 response
        and itself when passed to the validation endpoint.
        """
        client = APIClient(enforce_csrf_checks=True)
        orig_token = self.get_token('test_user', "testing")

        # Now try to get a refreshed token
        response = client.post( reverse(
                "token-verify",

            ), {'token': orig_token},
                               format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['token'], orig_token)

    def test_verify_jwt_fails_with_bad_token(self):
        """
        Test that an invalid token will fail with the correct error.
        """
        client = APIClient(enforce_csrf_checks=True)

        token = "i am not a correctly formed token"

        response = client.post(reverse('token-verify'), {'token': token},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegexpMatches(response.data['non_field_errors'][0],
                                 'Error decoding signature')


    def test_verify_jwt_fails_with_missing_user(self):
        """
        Test that an invalid token will fail with a user that does not exist.
        """
        client = APIClient(enforce_csrf_checks=True)

        user = User.objects.create_user(
            email='jsmith@example.com', username='jsmith', password='password')

        token = self.get_token('jsmith', 'password')
        # Delete the user used to make the token
        user.delete()

        response = client.post(reverse('token-verify'), {'token': token},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegexpMatches(response.data['non_field_errors'][0],
                                 "User doesn't exist")


