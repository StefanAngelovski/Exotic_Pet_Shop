document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.category-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target); // Stop observing once animated
            }
        });
    }, { threshold: 0.2 });

    cards.forEach(card => observer.observe(card));
});