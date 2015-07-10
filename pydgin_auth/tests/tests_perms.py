from django.test import TestCase
from django.db import router
from django.contrib.auth.models import User, Group
from django.test.client import RequestFactory, Client


class PydginAuthTest(TestCase):

    multi_db = True

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='EVERYONE')
        self.user = User.objects.create_user(
            username='test_user', email='test@test.com', password='test_pass')

    def test_routers(self):
        print('running test_routers')
        self.original_routers = router.routers

        routers = []
        for router_ in self.original_routers:
            routers.append(router_.__class__.__name__)

        self.assertTrue('AuthRouter' in routers, "Found AuthRouter in routers")
        self.assertTrue('DefaultRouter' in routers, "Found DefaultRouter in routers")

    def test_login(self):
        print('running test_login')
        response = self.client.get('/accounts/login?next=/human_GRCh38/', follow=True)
        # check if redirected to login
        self.assertTemplateUsed(response, 'registration/login.html')

        response = self.client.post('/accounts/login/', {'username': 'test_invalid', 'password': 'test_pass'})
        self.assertTrue(response.status_code, "200")
        response_string = response.content.decode('utf-8')
        self.assertTrue("The username and password provided is not valid/recognised" in response_string)

        response = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test_pass'})
        self.assertTrue(response.status_code, "200")
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], '1')

    def test_register_user(self):
        print('running test_register_user')
        response = self.client.get('/accounts/register/', follow=True)
        # check if redirected to registration page
        self.assertTemplateUsed(response, 'registration/registration_form.html')
