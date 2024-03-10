document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("registrationForm");
    form.addEventListener("submit", function(event) {
        let isValid = true; // Flag to determine if the form is valid
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        // Clear previous error messages
        document.getElementById("usernameError").textContent = '';
        document.getElementById("passwordError").textContent = '';
        document.getElementById("confirmPasswordError").textContent = '';

        // Username validation
        if (username.length < 5 || username.length > 16) {
            document.getElementById("usernameError").textContent = "Username must be between 5 and 16 characters.";
            isValid = false;
        }

        // Password validation
        if (password.length < 8 || !/[0-9]/.test(password) || 
            !/[A-Z]/.test(password) || !/[a-z]/.test(password)) {
            document.getElementById("passwordError").textContent = "Password must be at least 8 characters and include a number, an uppercase letter, and a lowercase letter.";
            isValid = false;
        }

        // Confirm password validation
        if (password !== confirmPassword) {
            document.getElementById("confirmPasswordError").textContent = "Passwords do not match.";
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
});