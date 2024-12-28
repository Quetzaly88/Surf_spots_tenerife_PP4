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
                        return; //stop further checks
                    }

                    //check if passwords match
                    if (password1 !== password2) {
                        alert("The passwords don't match!");
                        event.preventDefault(); //prevent form submission
                        return; //stop further checks
                    }

                    //check if email is valid using javascript code to validate email. 
                    const emailPattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                    if (!emailPattern.test(email)) {
                        alert("Please enter a valid email");
                        event.preventDefault(); //prevent from submission
                    }
                });
            }

            //select the surf post creation form
            const createPostForm = document. getElementById('create-post-form');

            //add event listener for creating a surf post
            if (createPostForm) {
            createPostForm.addEventListener('submit', async function (event) {
                    event.preventDefault();

                    // Get the values form fields values
                    const title = createPostForm.querySelector('#title').value;
                    const location = createPostForm.querySelector('#location').value;
                    const description = createPostForm.querySelector('#description').value;
                    const best_seasons = createPostForm.querySelector('#best_seasons').value;
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                    //validate required fields
                    if (!title || !location || !description) {
                        alert("All required fields must be filled!");
                        return;
                    }

                    try {
                        //send the POST request with JSON payload
                        const response = await fetch('/api/surf_spots/create/', {
                            method: "POST",
                            headers: {
                                'Content-Type': 'application/json', //ensured JSON format
                                'X-CSRFToken': csrfToken, // CSRF token
                            },
                            body: JSON.stringify({
                                title,
                                location,
                                description,
                                best_seasons,
                            }),
                        });

                        // handle the response
                        if (response.ok) {
                            displaySuccess("Surf spot created successfully!");
                            createPostForm.reset();
                        } else {
                            const errorData = await response.json();
                            displayError(errorData.error || "An unexpected error occurred.");
                        }
                    } catch (error) {
                        // Handle unexpected errors
                        console.error("Error during fetch:", error);
                        alert("An unexpected error occurred.");
                    }
                });
            }

                function displayError(message) {
                    const errorElement = document.querySelector('#error-message');
                    if (errorElement) {
                        errorElement.innerText = message;
                        errorElement.style.display = 'block';
                    }
                }

                // Function to display success messages. github AI
                function displaySuccess(message) {
                    const successElement = document.querySelector('#success-message');
                    if (successElement) {
                        successElement.innerText = message;
                        successElement.style.display = 'block';
                    }
                    const errorElement = document.querySelector('#error-message');
                    if (errorElement) {
                        errorElement.style.display = 'none';
                    }
                }
            });