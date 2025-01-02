/* jshint esversion: 8 */

document.addEventListener('DOMContentLoaded', function () {
            //Select the registration form element
            const registrationForm = document.querySelector('form');

            //add event listener for form submition (for user registration validation)
            if (registrationForm) {
                registrationForm.addEventListener('submit', function (event) {
                    const email = registrationForm.querySelector('input[name="email"]').value;
                    const username = registrationForm.querySelector('input[name="username"]').value;
                    const password1 = registrationForm.querySelector('input[name="password1"]').value;
                    const password2 = registrationForm.querySelector('input[name="password2"]').value;

                    // check if any fields are empty
                    if (!email || !username || !password1 || !password2) {
                        alert("All fields must be filled"); //show error message
                        event.preventDefault(); //prevent submission
                        return;
                    }

                    //check if passwords match
                    if (password1 !== password2) {
                        alert("The passwords don't match!");
                        event.preventDefault(); //prevent form submission
                        return; //stop further checks
                    }

                    //validate email format
                    const emailPattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                    if (!emailPattern.test(email)) {
                        alert("Please enter a valid email");
                        event.preventDefault(); //prevent from submission
                    }
                });
            }

            //validate the surf post creation form
            const createPostForm = document.getElementById('create-post-form');

            if (createPostForm) {
            createPostForm.addEventListener('submit', function (event) {

                    // Get the values form fields values
                    const title = createPostForm.querySelector('#title').value;
                    const location = createPostForm.querySelector('#location').value;
                    const description = createPostForm.querySelector('#description').value;
                    const best_seasons = createPostForm.querySelector('#best_seasons').value;

                    //validate required fields
                    if (!title || !location || !description || !bestSeasons) {
                        alert("All required fields must be filled!");
                        event.preventDefault();
                    }
                });
            }
        });