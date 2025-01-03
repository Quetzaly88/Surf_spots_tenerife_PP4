21 dec
Migration Issue. Inconsisten migration history. 
   When attempting to run **python manage.py migrate** was encountered an error. 
   The error indicated that the admin migration was applied before the migration for the sustom user model. This resulted in an inconsistent migration history. 
   The SQLite database was installed with hope that the issue was resolved but it didn'st work. 
   
   Solution: Database reset(rm db.sqlite3)
            Migration cleanup (rm users_account/migrations/0001_initial.py)
            Recreating migrations (python manage.py makemigrations users_account)
            Applying migrations (python manage.py migrate)
After the migration issue was resolved the terminal accepted commands and everything return to normal. 

I believe this issue was the result of me just doing the migrations that the terminal was suggesting. 



22 dec
https://www.w3resource.com/javascript/form/email-validation.php
javascript code

25 dec
**Errors:** 
Template doesn't exist: 
   The users_account/login.html template was not loading because of incorrect configurations.
   I corrected the directory structure with the new templates folder for login.html and register.html.

403 error:
    CSRF Verification failed: I found out that its purpose was for protection preventing external or malicious users to submit unauthorized POST requests to the server. 
    I added trusted URL, disable secure cookies for development and adding the csrf tokens. 

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

-----------------------------------------26 dec
**TESTING PROCESS**

This project includes the tests suited for the core functionality:
    - user registration
    - login
    - logout
The tests verify that the users can interact with the application as intended, with validation fot successful and error scenarios. 

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
   - A tst user (testuser) is created in the setUp method to simulate login and logout scenarios.

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


**How to run the tests?**
1. Run "python3 manage.py test"
2. The output will display the status of each test, indicating if is passed or if it has failed. 

* Testing in Django. https://docs.djangoproject.com/en/5.1/topics/testing/overview/
* Teast case class. https://docs.djangoproject.com/en/5.1/topics/testing/tools/#testcase
* User creation form. https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.forms.UserCreationForm

For Testing:
Errors: Installed black "pip install black". integrate "Black" with pre-commit hooks to ensure your code is formatted before each commit. pip install pre-commit. https://youtu.be/c5eaobs27yk?feature=shared. Commitment issues arised so I erased Black, commitment hooks and the virtual environment. 
I Used Copilot Github AI for some errors but it did.t help me.


https://jshint.com/. Javascript validation. using jshint version 8 



3 Jan. User Story 3
Task 1. about pagination
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