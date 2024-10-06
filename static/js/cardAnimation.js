document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.category-card');

    function animateCards(index = 0) {
        if (index < cards.length) {
            setTimeout(() => {
                cards[index].classList.add('animate');
                animateCards(index + 1);
            }, 60 * index);
        }
    }

    animateCards();
});