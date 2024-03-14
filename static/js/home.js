function centerAndStyleUsername() {
    var usernameElement = document.querySelector('.user-info .username');
    if (usernameElement) {
        // Style the username
        usernameElement.style.color = 'white'; // Example style
        usernameElement.style.fontSize = '1.2rem'; // Example style
        usernameElement.style.marginRight = '50%'; // Example style

        // Position the username in the center of the screen
        usernameElement.style.position = 'fixed'; // Use 'fixed' for viewport-relative positioning
        usernameElement.style.left = '50%';
        usernameElement.style.right = '50%';
        usernameElement.style.marginLeft = 'auto';
        usernameElement.style.marginRight = 'auto';
    }
}

// Call the function when the page loads and on window resize
window.onload = centerAndStyleUsername;
window.onresize = centerAndStyleUsername;
