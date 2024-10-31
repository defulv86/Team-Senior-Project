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

const errorMessage = document.querySelector('.error-message');
  if (errorMessage) {
    document.getElementById('username').classList.add('input-error');
    document.getElementById('passwd').classList.add('input-error');
  }


document.querySelectorAll('.txt_field input').forEach(input => {
  input.addEventListener('focus', () => {
      input.nextElementSibling.style.color = 'black';
  });

  input.addEventListener('blur', () => {
      input.nextElementSibling.style.color = '#999';
  });
});

document.querySelectorAll('.txt_field input').forEach(input => {
    input.addEventListener('keyup', function(event) {
      const warningElement = this.closest('.txt_field').querySelector('.caps-lock-warning');
      // Use closest to search up the DOM tree to find the warning element within the .txt_field
      if (event.getModifierState("CapsLock")) {
        warningElement.style.display = 'block';
      } else {
        warningElement.style.display = 'none';
      }
    });

    input.addEventListener('blur', function() {
      const warningElement = this.closest('.txt_field').querySelector('.caps-lock-warning');
      warningElement.style.display = 'none'; // Hide warning on blur
  });
});