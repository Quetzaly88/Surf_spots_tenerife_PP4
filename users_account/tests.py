from django.test import TestCase
from django.urls import reverse
from .models import NovaUser, SurfSpot, Comment, ModerationLog
#from django.core.paginator import Paginator


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
        self.assertTrue(NovaUser.objects.filter(username="newuser").exists())

    def test_user_login_logout(self):
        """
        Tests login and logout functionality in one function for less use of code
        """
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "password444",},
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
                category="For Everyone",
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

    def test_create_surf_spot(self):
        """
        Test creating a valid surf spot with a category
        """
        response = self.client.post(
            reverse("home"),
            {
                "title": "New Spot",
                "location": "New location",
                "description": "A great spot for surfing.",
                "best_seasons": "Winter",
                "category": "Beginner", #new category
            },
        )
        self.assertEqual(response.status_code, 302) # redirect after success.
        self.assertTrue(SurfSpot.objects.filter(title="New Spot", category="Beginner").exists())


class CommentTests(TestCase):
    @classmethod # method runs once for the entire test class. More efficient. 
    def setUpTestData(cls):
        """
        Set up initial data for all test methods.
        Runs once for the entire test class.
        """
        # Create a test user
        cls.user = NovaUser.objects.create_user(
            username="testuser",
            email="testuser@anemail.com",
            password="password444",
        )

        # Create a test surf spot
        cls.surf_spot = SurfSpot.objects.create(
            title="Test Surf Spot",
            location="Test location",
            description="A great surf spot",
            best_seasons="Winter",
            category="For Everyone",
            user=cls.user,
        )


    def setUp(self):
        """
        Log in the user before each test.
        This runs before every test method
        """
        self.client.login(username="testuser", password="password444")


    def test_add_comment_valid_and_invalid(self):
        """
        Test adding a valid comment and handling an invalid (empty) comment.
        """
        # Test valid comment
        response = self.client.post(
            reverse("add_comment", args=[self.surf_spot.id]),
            {"content": "This is a valid comment."}, 
        )
        self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertTrue(Comment.objects.filter(content="This is a valid comment.").exists())

        # Test invalid (empty) comment
        response = self.client.post(
            reverse("add_comment", args=[self.surf_spot.id]),
            {"content": ""}, # Empty content
        )
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertContains(response, "This field is required.")
        self.assertFalse(Comment.objects.filter(content="").exists())


    def test_add_comment_requires_login(self):
        """
        Test that only logged in users can add comments.
        """
        self.client.logout() # Log out the test user
        response = self.client.post(
            reverse("add_comment", args=[self.surf_spot.id]),
            {"content": "This is a comment."},
        )
        #self.assertEqual(response.status_code, 302)  # Check for redirect after success
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('add_comment', args=[self.surf_spot.id])}")
        self.assertFalse(Comment.objects.filter(content="This is a comment.").exists())

class SurfSpotCategoryTests(TestCase):
    def setUp(self):
        """
        Set up a test user and surf spots with different categories for testing.
        """
        self.user = NovaUser.objects.create_user(
            username="testuser",
            email="testuser@anemail.com",
            password="password444",
        )
        self.client.login(username="testuser", password="password444")
        
        SurfSpot.objects.create(
            title="Beginner Spot",
            location="Beach A",
            description="A beginner-friendly spot.",
            best_seasons="Summer",
            category="Beginner",
            user=self.user,
        )

        SurfSpot.objects.create(
            title="Advanced Spot",
            location="Beach B",
            description="A spot for advanced surfers.",
            best_seasons="Winter",
            category="Advanced",
            user=self.user,
        )
        
    def test_filtering_by_category(self):
        """
        Test filtering returns correct surf spots for selected category
        """
        response = self.client.get(reverse("home"), {"category": "Beginner"})
        self.assertContains(response, "Beginner Spot")
        self.assertNotContains(response, "Advanced Spot")

    def test_no_filter_displays_all(self):
        """
        Test all surf spots are displayed when no category filter is applied.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Beginner Spot")
        self.assertContains(response, "Advanced Spot")


# Tests to validate ModerationLog
# admins can delete posts/comments. Users can delete own posts/comments, no unauthorized. 
class ModerationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for all moderation tests. 
        """
        # Create a regular user
        cls.user = NovaUser.objects.create_user(
            username="testuser",
            email="testuser@anemail.com",
            password="password444",
        )

        #Create an admin user
        cls.admin = NovaUser.objects.create_superuser(
            username="adminuser",
            email="adminuser@anemail.com",
            password="adminpassword",
        )

        # Create a surf spot by a regular user
        cls.surf_spot = SurfSpot.objects.create(
            title="Test Surf Spot",
            location="Test location",
            description="A great surf spot",
            best_seasons="Winter",
            category="For Everyone",
            user=cls.user,
        )

        # Create a comment on the surf spot by the regular user
        cls.comment = Comment.objects.create(
            surf_spot=cls.surf_spot,
            user=cls.user,
            content="This is a test comment"
        )

    def setUp(self):
        """
        Log out the user before each test to ensure a clean state. 
        """
        self.client.logout()

    def test_admin_can_delete_any_post_and_comment(self):
        """
        Test that an admin can delete any post and any comment. 
        Ensure that actions are logged in ModerationLog. 
        """
        self.client.login(username="adminuser", password="adminpassword")

        # Delete the post
        response = self.client.post(reverse("delete_post", args=[self.surf_spot.id]))
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(SurfSpot.objects.filter(id=self.surf_spot.id).exists())

        # Delete comment
        response = self.client.post(reverse("delete_comment", args=[self.comment.id]))
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
        
        #check that both actions are logged
        self.assertTrue(
            ModerationLog.objects.filter(action_type="Deleted Post", moderator=self.admin).exists())
            
        self.assertTrue(
            ModerationLog.objects.filter(action_type="Deleted Comment", moderator=self.admin).exists())


    def test_user_cannot_delete_others_post_or_comment(self):
        """
        Test that a a regular user cannot delete another user's post or comment.
        """
        self.client.login(username="testuser", password="password444")

        # Create another surf spot and comment by the admin
        admin_surf_spot = SurfSpot.objects.create(
            title="Admin Post",
            location="Admin Location",
            description="An admin-only post",
            best_seasons="Summer",
            category="Advanced",
            user=self.admin,
        )
        admin_comment = Comment.objects.create(
            surf_spot=admin_surf_spot,
            user=self.admin,
            content="Admin-only comment."
        )


        # Try deleting admin's post
        response = self.client.post(reverse("delete_post", args=[admin_surf_spot.id]))
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(SurfSpot.objects.filter(id=admin_surf_spot.id).exists())
        
        # Try deleting admin's comment
        response = self.client.post(reverse("delete_comment", args=[admin_comment.id]))
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Comment.objects.filter(id=admin_comment.id).exists())
            