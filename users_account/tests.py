from django.test import TestCase
from django.urls import reverse
from .models import NovaUser, SurfSpot
from django.core.paginator import Paginator


class UserAuthTests(TestCase):
    def setUp(self):
        """
        Set up a test user for authentication tests
        """
        self.user = NovaUser.objects.create_user(
            username="testuser",
            email="testuser@anemail.com",
            password="password444",
        )
        #self.client.login(username="testuser", password="password444")


    def test_registration_valid(self):
        """
        Test that a valid registration redirects and creates a new user
        """
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@anemail.com",
                "password1": "astrongpassword",
                "password2": "astrongpassword",
            },
        )
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertTrue(
            NovaUser.objects.filter(username="newuser").exists()
        )  # User should be created

    def test_user_login_logout(self):
        """
        Tests login and logout functionality in one function for less use of code
        """
        #Test login
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "password444",
            },
        )
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertRedirects(response, reverse("home"))

        #Test logout
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertRedirects(response, reverse("login"))


class SurfSpotTests(TestCase):
    def setUp(self):
        """
        Set up a test user and create surf spots for testing. 
        """
        self.user = NovaUser.objects.create_user(
            username="testuser",
            email="testuser@anemail.com",
            password="password444",
        )
        self.client.login(username="testuser", password="password444")

        # Create 12 surf spots for pagination and detail view tests
        for i in range(12):
            SurfSpot.objects.create(
                title=f"Surf Spot {i+1}",
                location=f"Location {i+1}",
                description="A great spot.",
                best_seasons="Summer",
                user=self.user,
            )


    def test_pagination_first_and_last_page(self):
        """
        Test that pagination returns the correct number of posts per page
        and navigates between pages. Just the first and last page to reduce code. 
        """
        # Test first page
        response = self.client.get(reverse("home") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Surf Spot 1")
        self.assertContains(response, "Surf Spot 5")
        self.assertNotContains(response, "Surf Spot 6") #Should not be on page 1

        # Test last page
        response = self.client.get(reverse("home") + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Surf Spot 11")
        self.assertContains(response, "Surf Spot 12")
        self.assertNotContains(response, "Surf Spot 5") #Should not be on page 2


    def test_surf_spot_detail_view(self):
        """
        Test that the detail view returns the correct surf spot details.
        """
        # Fetch the detail view for a specific surf spot
        spot = SurfSpot.objects.get(title="Surf Spot 1")
        response = self.client.get(reverse("surf_spot_detail", args=[spot.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Surf Spot 1")
        self.assertContains(response, "Location 1")
        self.assertContains(response, "A great spot.") # updated description
        self.assertContains(response, "Summer")
        self.assertContains(response, self.user.username)


    def test_create_surf_spot(self):
        """
        Test that a valid surf spot can be created and appears in home page.
        """
        response = self.client.post(
            reverse("home"),
            {
                "title": "New Spot",
                "location": "New location",
                "description": "A great spot for surfing.",
                "best_seasons": "Winter",
            },
        )
        self.assertEqual(response.status_code, 302) # redirect after success.
        self.assertTrue(SurfSpot.objects.filter(title="New Spot").exists())

        # Verify the surf spot appears in the homepage
        response = self.client.get(reverse("home"))
        self.assertContains(response, "New Spot")
        self.assertContains(response, "A great spot for surfing.")




    #     self.assertEqual(response.status_code, 302) #redirect after success
    #     self.assertTrue(SurfSpot.objects.filter(title="Valid title").exists())

    # def test_create_surf_spot_invalid_title(self):
    #     response = self.client.post(
    #         reverse("home"),
    #         {
    #             "title": "T" * 51, # Exceeding max_lenght
    #             "location": "Valid location",
    #             "description": "A good spot.",
    #             "best_seasons": "Summer",
    #         },
    #     )
    #     self.assertEqual(response.status_code, 200) # Stays on the page
    #     self.assertContains(response, "Ensure this value has at most 50 characters")

    # # test valid user registration
    # def test_end_to_end_flow(self): 
    #     #register a new user
    #     self.client.logout()
    #     response = self.client.post(
    #         reverse("register"),
    #         {
    #             "username": "newuser",
    #             "email": "newuser@example.com",
    #             "password1": "password123",
    #             "password2": "password123",
    #         },
    #     )
    #     self.assertEqual(response.status_code, 302)  # Redirect after success
    #     self.assertTrue(NovaUser.objects.filter(username="newuser").exists())
    
    #     # Login as the new user
    #     self.client.login(username="newuser", password="password123")

    #     # Create a new surfspot
    #     response = self.client.post(
    #         reverse("home"),
    #         {
    #             "title": "New Spot",
    #             "location": "New location",
    #             "description": "A great spot for surfing.",
    #             "best_seasons": "Winter",
    #         },
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(SurfSpot.objects.filter(title="New Spot").exists())

    #     # Verify the surf spot appears in the homepage
    #     response = self.client.get(reverse("home"))
    #     self.assertContains(response, "New Spot")
    #     self.assertContains(response, "A great spot for surfing.")

    


    # # test invalid user registration
    # def test_registration_invalid(self):
    #     response = self.client.post(
    #         reverse("register"),
    #         {
    #             "username": "",
    #             "email": "invalid-email",
    #             "password1": "aweirdpassword",
    #             "password2": "nomatchpassword",
    #         },
    #     )
    #     self.assertEqual(response.status_code, 200)  # Check for redirect after success
    #     self.assertContains(
    #         response, "The two password fields didn’t match.", status_code=200
    #     )

    # # # test valid user login
    # # def test_user_login_valid(self):
    # #     response = self.client.post(
    # #         reverse("login"),
    # #         {
    # #             "username": "testuser",
    # #             "password": "password444",
    # #         },
    # #     )
    # #     self.assertEqual(response.status_code, 302)  # Check for redirect after success
    # #     self.assertRedirects(response, reverse("home"))

    # # # test invalid user login
    # # def test_user_login_invalid(self):
    # #     response = self.client.post(
    # #         reverse("login"),
    # #         {
    # #             "username": "testuser",
    # #             "password": "invalidpassword",
    # #         },
    # #     )
    # #     self.assertEqual(response.status_code, 200)  # No redirect. remains in login page
    # #     self.assertContains(response, "Invalid username or password", status_code=200)

    # # # test case for logout:
    # # def test_user_logout(self):
    # #     # login user.
    # #     self.client.login(username="testuser", password="password444")
    # #     # logout request.
    # #     response = self.client.get(reverse("logout"))
    # #     self.assertEqual(response.status_code, 302)  # Check for redirect after success
    # #     self.assertRedirects(response, reverse("login"))

    # # Test access for logged out users cannot access ptotected pages
    # def test_home_page_requires_login(self):
    #     """
    #     Test that the page requires login and redirects unauthenticated user to login page
    #     """
    #     self.client.logout()
    #     response = self.client.get(reverse("home"))
    #     self.assertEqual(response.status_code, 302)
    #     # redirect should include "next" parameter in the url
    #     self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")


