const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('passwd');

// Username field focus and blur events
usernameInput.addEventListener('focus', () => {
    usernameInput.placeholder = 'Enter your username';
});
usernameInput.addEventListener('blur', () => {
    usernameInput.placeholder = '';  // Clear the placeholder when the user leaves the field
});

// Password field focus and blur events
passwordInput.addEventListener('focus', () => {
    passwordInput.placeholder = 'Enter your password';
});
passwordInput.addEventListener('blur', () => {
    passwordInput.placeholder = '';  // Clear the placeholder when the user leaves the field
});



