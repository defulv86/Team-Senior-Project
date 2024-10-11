document.querySelector('.toggle-button').addEventListener('click', function() {
    document.querySelector('.sidebar').classList.toggle('collapsed');
    document.querySelector('.main-content').classList.toggle('collapsed');
});
