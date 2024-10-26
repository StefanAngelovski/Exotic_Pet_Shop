document.addEventListener('DOMContentLoaded', function () {
    const animalCards = document.querySelectorAll('.category-card');
    const viewAllButton = document.getElementById('view-all-button');
    const toggleButton = document.getElementById('toggle-button');
    const initialCount = 6; // Number of cards to show initially
    let showingAll = false; // Track the current state (whether showing all or less)

    // Hide all cards after the initial count
    function showInitialCards() {
        animalCards.forEach((card, index) => {
            if (index >= initialCount) {
                card.style.display = 'none'; // Hide cards after the first 6
            }
        });
    }

    // Show all cards
    function showAllCards() {
        animalCards.forEach(card => {
            card.style.display = 'flex';
        });
    }

    // Function to handle showing/hiding the "View All" button
    function toggleViewAllButton(categoryId) {
        // Only show "View All" button if "All Animals" is selected
        if (categoryId === 'all' && animalCards.length > initialCount) {
            viewAllButton.style.display = 'flex'; // Show the button
            showInitialCards();
        } else {
            viewAllButton.style.display = 'none'; // Hide the button
            showAllCards(); // Show all cards if another category is selected
        }
    }

    toggleButton.addEventListener('click', function () {
        if (showingAll) {
            // If currently showing all, hide extra cards and change button text to "View All"
            showInitialCards();
            toggleButton.textContent = `View All ${animalCards.length} Animals`;
            showingAll = false;
        } else {
            // If currently showing less, show all cards and change button text to "View Less"
            showAllCards();
            toggleButton.textContent = 'View Less';
            showingAll = true;
        }
    });

    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('category-item')) {
            const categoryId = e.target.getAttribute('data-category-id');
            toggleViewAllButton(categoryId);
        }
    });

    toggleViewAllButton('all');
});
