### SURF SPOTS TENERIFE

A **FULL-STACK web application** that allows users to share, view, and discuss surf spots in Tenerife. 
The platform supports user-generated content, such as surf spots details and community comments. It features category-baseed filtering, pagination, and role-based permissions. This application is built using Django framework following the MVC architecture. 
The application is mobile-friendly and includes admin moderation tools. 

--- 

# Table of Contents
1. Features
2. User Stories
3. UX Design and Wireframes
4. Data models
5. Technologies used
6. Testing
7. Deployment
8. Known Issues
9. Future Enhancements
10. Sources

---

# 1. Features
* User Registration & Authentication:
   - The user can register, log-in and log-out securely. - Role-based permissions are implemented, alowing only authorized user to create. edit, delete posts and comments.
   - Admins can delete any content.

* Posts and Comments:
   - Logged-in users can create a new surf spot post, including a title, location, description, category and best seasons.
   - Logged-in users can post comments on surf spots. 
   - Logged-in users can edit and delete their own comments and posts. 

* Filtering and pagination
   - Posts can be filtered by category. 
   - The pagination improves loading and displays 5 posts per page at its max. 

* Moderation
   - Admins can delete any comment or post.
   - All admin actions are logged via ModerationLog model. 

* Responsive Design
   - Mobile friendly layout
   - Simple navigation and clear feedback messages. 


# 2. User Stories
1. User registration and login
   As a user, I want to create an account and log in, so that I can post and comment about surf spots.

2. Post Surf Spots
   As a user, I want to share surf spots with the community, so that others can discover and learn about new locations.

3. Commenting on posts
   As a user I can I want to browse and view surf spots, so that I can explore and learn about surfing locations.

4. Discussing surf spots
   As a user, I want to comment on surf spots, so that I can share my opinions and learn from others.

5. Filtering Surf Spots by Categories
   As an user, I want to filter surf spots by categories, so that I can find surf spots suited to my skills.

6. Moderating content
   As an admin I can manage posts and comments, so that I can ensure the community follows the guidelines.

7. Exploring on mobile
   As a user, I want the platform to work well on my mobile device, so that I can browse surf spots on the go.

8. Deploying the platform
   As a user I want the platform to be live and functional so that I can access it anytime, anywhere.

# 3. UX Design & Wireframes

**Color Palette**

**Fonts**



**Layout Decisions**
   - Created base.html to ensure consistent layout and styling across templates.
   - Navigation and user feedback messages are placed at the top of every page. 
   - Surf cards are separated using each spot.

**Wireframes**

# 4. Data Models
   This application uses Django's ORM to define and manage the following models: 

   **NovaUser** 
      - A custom user model extending Django's AbstractUser.
      - Allows future customization for user-specific features. 
   **SurfSpot**
      - Represents a surf location shared by users.
      - Includes fields like title, location, description, best_seasons, category and timestamps. 
      - Linked to NovaUser via a ForeignKey (user). 
   **Comment**
      - Represents user comments on surf spots. 
      - Linked to both the SurfSpot and the NovaUser who wrote the comment. 
   **ModerationLog**
      - Stores admin actions like deleted posts or commeents.
      - Records the moderator, target content and timestamp for audit purposes. 

# 5. Technologies used
   Backend: Django (Python)
   Frontend: HTML, CSS, JavaScript
   Version Control: Github, VS code. 
   Deployment: Heroku
   Testing: Django's built-in 'TestCase'


# 6. Testing
**TESTING PROCESS**
   Testing is implemented using Django's buitt-in 'TestCase' framework. All core features and user flows are covered, ensuring robust functionality, secure access and expected behaviour for both users and admins. 

   Areas covered: 
      - User registration, login, logout
      - Post creation, editing, deletion
      - Comment creation, editing, deletion
      - Pagination (5 posts per page)
      - Category filtering
      - Permissions (admin vs user)
      - Moderation logging (admin only actions)

   How to run tests: 
      Write command: python3 manage.py test

   * Features Tested:

      1. User Registration:
         - Valid registration: Tests if a new user is successfully created when the data submited is valid.
         - Invalid inputs (missing fields, mismatched passwords) return error messages. 

      2. User Login & Logout: 
         - Valid Login: Verifies that useers can login with the correct credentials.
         - Invalid login: The application prevents login with incorrect credentials and displays error message. 
         - Logged in users can logout successfully.

      3. Access Control: 
         - Unauthenticated users trying to acceess protected routes are redirected to the login page with the ?next= parameter. 

      4. Surf Spot Posts:
         - Users can create new posts with all required fields.
         - Users can delete or edit their own posts.
         - Users can't modify other user's posts.
         - Admins can edit or delete any post.

      5. Comments:
         - Logged-in users can post comments.
         - Empty or invalid comments return appropiate errors.
         - Users can edit or delete their own comments.
         - Users cannot delete commetns made by others.
         - Admins can delete any comment. 

      6. Pagination:
         - Verifies that only 5 posts are displayed per page.
         - Tests first and last pages for correct content. 
      
      7. Category Filtering:
         - Tests that selecting a category only shows matching posts.
         - All posts ate shown when no filter is applied. 
      
      8. Moderation Logging
         - Admin deletions of posts and comments are saved in the ModerationLog model.
         - Each log entry includes the action type, moderator, affected user, content snippet and timestamp. 


# 7. Deployment
   - Create an account in Heroku
   - Install heroku CLI and login
   - Create a new heroku app.
   - Save environment variables in .env. Use python-decouple.
   - Run python manage.py migrate and python manage.py collectstatic.
   - Push to Heroku
   - Set config vars on Heroku dashboard. 


# 8. Known Issues

   * Migration Issue. Inconsisten migration history. 
      When attempting to run **python manage.py migrate** was encountered an error. 
      The error indicated that the admin migration was applied before the migration for the sustom user model. This resulted in an inconsistent migration history. 
      The SQLite database was installed with hope that the issue was resolved but it didn'st work. 
   
      Solution: Database reset(rm db.sqlite3)
         - Migration cleanup (rm users_account/migrations/0001_initial.py)
         - Recreating migrations (python manage.py makemigrations users_account)
         - Applying migrations (python manage.py migrate)
            After the migration issue was resolved the terminal accepted commands and everything return to normal. 

   * Template doesn't exist: 
      The users_account/login.html template was not loading because of incorrect configurations.
      I corrected the directory structure with the new templates folder for login.html and register.html.

   * 403 error:
      CSRF Verification failed: I found out that its purpose was for protection preventing external or malicious users to submit unauthorized POST requests to the server. 
      I added trusted URL, disable secure cookies for development and adding the csrf tokens. 


   * About pagination
      This was new to me.
      This task involved creating a paginated API endpoint that lists all surf spots. The purpose of pagination is to improve loading times by displaying a limited number of posts per page. 

   * Endpoint URL:
    https://8000-quetzaly88-surfspotsten-jr4iym5ywcp.ws.codeinstitute-ide.net/surf_spots/paginated/?page=1
   
      Features:
      The API returns a list of surf spots wuth their title, location and creation date. 
      Pagination is implemented with a default of 5 posts per page.
      If there aren't no surf spots, the API returns an empty list. 


### Project Fixes & Deployment Configuration after review: 
* Environment Variables:
   For security best practices, sensitive settings have been moved to a .env file and accessed using python-decouple. This keeps secrets out of version control.
   Variables used: 
      - SECRET_KEY
      - DEBUG

   Accessed (settings.py) using:

         from decouple import config
         SECRET_KEY = config('SECRET_KEY')
         DEBUG = config('DEBUG', cast=bool)

   The .env file is listed in .gitignore and never pushed to GitHub.  

* Static files (CSS, JavaScript, images):
   Static files were configured work in both development and production using WhiteNoise and Django's static settings: 

         STATIC_URL = '/static/'
         STATICFILES_DIRS = [BASE_DIR / 'static']
         STATIC_ROOT = BASE_DIR / 'staticfiles'

   - Command to collect static files:

         % python manage.py collectstatic 
   
      This collects all static assets into the /staticfiles/ directory, which is served by Heroku in production. 

   - DISABLE_COLLECTSTATIC = 1 is removed from config vars in Heroku. This variable skips static file collection, which breaks CSS, images and JavaScript in production. 


* Middleware configuration (in settings.py):

   MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
   ...]

* Heroku Setup & Commands
   - To prepare and deploy your app on Heroku: 

         % heroku run python manage.py migrate --app surf-spots-tenerife

         % heroku run python manage.py collectstatic --app surf-spots-tenerife

* Styling Issues Fix
   - CSS and JS not loading
   - 404 errors in DevTools - Static files not found. 

   Solution (run in terminal):

      heroku run --app surf-spots-tenerife "python manage.py collectstatic --noinput"

   Explanation: 
      - Heroku run: Executes a one-time command on the Heroku dyno (remote server).

      - --app surf-spots-tenerife: Specifies which Heroku app to run the command on.

      - "python manage.py collectstatic": Tells Django to gather all static files into the /staticfiles/ directory.

      - --noinput: Skips any interactive prompts during collection (e.g., "Overwrite warnings").


# 10. SOURCES
https://www.surfmarket.org/es/olas/europa/canarias/tenerife
https://ron.sh/handling-custom-django-error-pages-the-proper-way/?utm_source=chatgpt.com
https://coolors.co/f79256-fbd1a2-7dcfb6-00b2ca-
https://docs.djangoproject.com/en/5.1/topics/logging/
https://docs.djangoproject.com/en/5.1/topics/testing/
https://docs.djangoproject.com/en/5.1/
https://youtu.be/XRRuWEDLwAE?feature=
https://youtu.be/UpssHYl6bjA?feature=shared
https://www.youtube.com/watch?v=_uQrJ0TkZlc
https://www.youtube.com/@programmingwithmosh

https://docs.djangoproject.com/en/5.2/howto/static-files/
https://docs.djangoproject.com/en/5.2/ref/django-admin/#collectstatic
https://devcenter.heroku.com/articles/django-assets
