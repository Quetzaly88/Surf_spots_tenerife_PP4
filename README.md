# SURF SPOTS TENERIFE

A FULL-STACK web application where users can share, view, and discuss surf spots in Tenerife. 
The app allows users to post surf spots details. Also, the users can write comments on posts and like this interact with the community. 
The user friendly interface provides categories which can be filtered and even pagination for a better reading experience. 
This app follows the MVC framework using Django. 

## Table of Contents
1. Features
2. User Stories
3. UX Design and Wireframes
4. Technologies used
5. Testing
6. Deployment
7. Known Issues
8. Future Enhancements
9. Sources

---

### 1. Features
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


### 2. User Stories
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
* Color and Typography
   - Palette:
   - Fonts: 

* Layout Decisions
   - Created base.html to ensure consistent layout and styling across templates.
   - Navigation and user feedback messages are placed at the top of every page. 
   - Surf cards are separated using each spot.

* Wireframes


# 4. Technologies used
   Backend: Django (Python)
   Frontend: HTML, CSS, JavaScript
   Version Control: Github, VS code. 
   Deployment: Heroku
   Testing: Django's built-in 'TestCase'

### 4. Testing
**TESTING PROCESS**

Tests are written using Django’s built-in testing tools. Tests cover:

- Registration, login, logout
- Post creation, editing, deletion
- Comment creation, editing, deletion
- Pagination
- Category filtering
- Permissions (admin vs user)
- Moderation logging

```bash
# Run tests
python3 manage.py test

**Features Tested**

   1. User Registration
   - Valid registration: Tests if a new user is successfully created when the data submited is valid.
   - Invalid registration: Tests if invalid inputs occur, such as missing username, invalid email, or mismatched passwords. 

   2. User Login
   - Valid Login: Verifies that useers can login with the correct credentials.
   - Invalid login: The application prevents login with incorrect credentials and displays error message. 

   3. User logout
   - Ensures that logged in users can logout and redirect to login page. 

**How does the tests work?**

   1. Setup
   - A testuser is created in the setUp method to simulate login and logout scenarios.

   2. User Registration
   - A POST request is made to the register URL with invalid and valid data. 
   - The tests confirm if the user is created and will procede with the correct response. 

   3. User Login
   - A POST request is made to the login URL with both valid and invalid credentials. 
   - The tests ensure proper rediretion or error messages. 

   4. User logout
   - A GET request is made to the logout URL, and the test verifies redirection to the login page. 

   5. Access Control
   - An anauthenticated user attempts to access a protected page. 
   - The test ensures the user is redirected to login page with a next parameter for redirection after login. 



### 5. Deployment
- Create an account in Heroku
- Install heroku CLI and login
- Create a new heroku app.
- Save environment variables in .env. Use python-decouple.
- Run python manage.py migrate and python manage.py collectstatic.
- Push to Heroku
- Set config vars on Heroku dashboard. 

### 6. Known Issues

* Migration Issue. Inconsisten migration history. 
   When attempting to run **python manage.py migrate** was encountered an error. 
   The error indicated that the admin migration was applied before the migration for the sustom user model. This resulted in an inconsistent migration history. 
   The SQLite database was installed with hope that the issue was resolved but it didn'st work. 
   
   Solution: Database reset(rm db.sqlite3)
            Migration cleanup (rm users_account/migrations/0001_initial.py)
            Recreating migrations (python manage.py makemigrations users_account)
            Applying migrations (python manage.py migrate)
After the migration issue was resolved the terminal accepted commands and everything return to normal. 

I believe this issue was the result of me just doing the migrations that the terminal was suggesting. 

* Template doesn't exist: 
   The users_account/login.html template was not loading because of incorrect configurations.
   I corrected the directory structure with the new templates folder for login.html and register.html.

403 error:
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


Post details view
Created API end point to displey the details of a specific surf spot. The endpoint quieris the database for a durfspot by its unique id. 
If the requested surf spot doesn't exist 404 error is returned
https://8000-quetzaly88-surfspotsten-jr4iym5ywcp.ws.codeinstitute-ide.net/surf_spots/detail/13/ #13 is the ID. 



* SOURCES
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


### Project Fixes & Deployment Configuration
* Environment Variables:
   For security best practices, sensitive settings have been moved to a .env file and accessed using python-decouple. 
   - SECRET_KEY
   - DEBUG

   These are now accessed (settings.py) using:
         from decouple import config

         SECRET_KEY = config('SECRET_KEY')
         DEBUG = config('DEBUG', cast=bool)

   The .env file is included in .gitignore and never pushed to version control. 

* Static files (CSS, JavaScript, images) were configured to load correctly in both development and production environments using Whitenoise and Django's static file settings:

   STATIC_URL = '/static/'
   STATICFILES_DIRS = [BASE_DIR / 'static']
   STATIC_ROOT = BASE_DIR / 'staticfiles'

   terminal: 
   % python manage.py collectstatic (This has collected static files which is necesary for Heroku to serve them in production)

   Middleware configuration:
   MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
   ...]

   terminal: 
   % heroku run python manage.py migrate --app surf-spots-tenerife
   % heroku run python manage.py collectstatic --app surf-spots-tenerife

* Add "Edit" feature to the posts. 
   Now the owners of their posts can edit their post and save it. Now is fully implemented and tested. 
Add "Edit comment" feature. 