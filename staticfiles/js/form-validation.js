// load DOM
document.addEventListener('DOMContentLoaded', function () {
    //Select the form element
    let form = document.querySelector('form');

    //add event listener for form submition
    form.addEventListener('submit', function (event) {
        //get the values of form inputs
        const email = form.querySelector('input[name="email"]').value;
        const username = form.querySelector('input[name="username"]').value;
        const password1 = form.querySelector('input[name="password1"]').value;
        const password2 = form.querySelector('input[name="password2"]').value;

        // check if any fields are empty
        if (!email || !username || !password1 || !password2) {
            alert("All fields must be filled"); //show error message
            event.preventDefault(); //no submission
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
});