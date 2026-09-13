// ================================
// Data Guardian AI Authentication
// ================================

// ---------- LOGIN ----------

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const email = document.getElementById("email").value;

        const password = document.getElementById("password").value;

        console.log("Login");

        console.log(email);

        console.log(password);

        alert("Login API will be connected soon.");

    });

}

// ---------- REGISTER ----------

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const fullname = document.getElementById("fullname").value;

        const email = document.getElementById("email").value;

        const password = document.getElementById("password").value;

        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {

            alert("Passwords do not match.");

            return;

        }

        console.log("Register");

        console.log(fullname);

        console.log(email);

        console.log(password);

        alert("Registration API will be connected soon.");

    });

}