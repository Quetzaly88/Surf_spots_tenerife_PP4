from django.test import TestCase
from django.urls import reverse
from .models import NovaUser

#TEMPLATE: https://docs.djangoproject.com/
class UserAuthTests(TestCase):
    def setUp(self):
        self.user = NovaUser.objects.create_user(
        username='testuser',
        email='testuser@anemail.com',
        password='password444',
        )

#test valid user registration
    def test_registration_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@anemail.com',
            'password1': 'astrongpassword',
            'password2': 'astrongpassword',
        })
        #https://forum.djangoproject.com/t/test-fails-with-assertionerror-302-200/31182
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertTrue(NovaUser.objects.filter(username='newuser').exists())  # User should be created

#test invalid user registration
    def test_registration_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'invalid-email',
            'password1': 'aweirdpassword',
            'password2': 'nomatchpassword',
        })
        #https://docs.djangoproject.com/en/stable/topics/forms/#field-data-validation
        #https://forum.djangoproject.com/t/test-fails-with-assertionerror-302-200/31182
        self.assertEqual(response.status_code, 200)  # Check for redirect after success
        self.assertContains(response, "The two password fields didn’t match.", status_code=200)

#test valid user login
    def test_user_login_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password444',
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertRedirects(response, reverse('home'))

#test invalid user login
    def test_user_login_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'invalidpassword',
        })
        self.assertEqual(response.status_code, 200)  # No redirect. remains in login page
        self.assertContains(response, "Invalid username or password", status_code=200)

# test case for logout: https://docs.djangoproject.com/en/stable/topics/testing/tools/#testcase
    def test_user_logout(self):
        #login user. 
        self.client.login(username='testuser', password='password444')
        #logout request. 
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertRedirects(response, reverse('login'))

#Test access for logged out users cannot access ptotected pages
    def test_home_page_requires_login(self): 
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        #redirect should include "next" parameter in the url
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")