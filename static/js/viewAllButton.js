document.addEventListener('DOMContentLoaded', function() {
    const animalCards = document.querySelectorAll('.category-card');
    const viewAllButton = document.getElementById('view-all-button');
    const toggleButton = document.getElementById('toggle-button');
    const initialCount = 6;
    let showingAll = false;

    function showInitialCards() {
        animalCards.forEach((card, index) => {
            if (index >= initialCount) {
                card.style.display = 'none';
            }
        });
        if (animalCards.length > initialCount) {
            viewAllButton.style.display = 'flex';
            toggleButton.textContent = `View All ${animalCards.length} Animals`;
        }
    }

    toggleButton.addEventListener('click', function() {
        if (showingAll) {
            showInitialCards();
        } else {
            animalCards.forEach(card => card.style.display = 'flex');
            toggleButton.textContent = 'View Less';
        }
        showingAll = !showingAll;
    });

    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('category-item')) {
            const categoryId = e.target.getAttribute('data-category-id');
            showingAll = false;
            if (categoryId === 'all') {
                showInitialCards();
            } else {
                viewAllButton.style.display = 'none';
                animalCards.forEach(card => card.style.display = 'flex');
            }
        }
    });

    showInitialCards();
});