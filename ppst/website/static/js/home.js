let lastScroll = 0;

// Smooth Scrolling Behavior
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('nav ul li a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    const nav = document.querySelector('nav');

    if (nav) {
        window.addEventListener('scroll', function () {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            if (scrollTop > lastScroll) {
                nav.classList.add('hidden');
            } else {
                nav.classList.remove('hidden');
            }

            lastScroll = scrollTop <= 0 ? 0 : scrollTop;
        });
    }
});
