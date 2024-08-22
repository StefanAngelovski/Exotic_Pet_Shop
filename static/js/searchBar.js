document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.querySelector('.search-icon');
    const searchBar = document.getElementById('search-input');
    const searchSuggestions = document.getElementById('search-suggestions');

    searchIcon.addEventListener('click', (event) => {
        event.preventDefault();
        searchBar.classList.toggle('active');
        if (searchBar.classList.contains('active')) {
            searchBar.focus();
        } else {
            searchSuggestions.style.display = 'none';
        }
    });

    // Close search bar when clicking outside
    document.addEventListener('click', (event) => {
        if (!searchBar.contains(event.target) && !searchIcon.contains(event.target)) {
            searchBar.classList.remove('active');
            searchSuggestions.style.display = 'none';
        }
    });

    // Global search function
    window.performSearch = function(searchTerm) {
        // This function will be implemented in index.html
        console.log('Searching for:', searchTerm);
    }

    // Handle search input
    searchBar.addEventListener('input', () => {
        const searchTerm = searchBar.value.toLowerCase();
        window.performSearch(searchTerm);

        // Fetch suggestions
        if (searchTerm.length > 0) {
            fetch(`/search/?query=${searchTerm}`)
                .then(response => response.json())
                .then(data => {
                    searchSuggestions.innerHTML = '';
                    data.forEach(animal => {
                        const suggestion = document.createElement('div');
                        suggestion.classList.add('suggestion-item');
                        suggestion.textContent = animal.name;
                        suggestion.addEventListener('click', () => {
                            window.location.href = `/animal/${animal.id}`;
                        });
                        searchSuggestions.appendChild(suggestion);
                    });
                    searchSuggestions.style.display = 'block';
                });
        } else {
            searchSuggestions.style.display = 'none';
        }
    });

    // Handle search submission
    searchBar.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            window.performSearch(searchBar.value);
            searchBar.value = ''; // Clear the search bar
            searchBar.classList.remove('active');
            searchSuggestions.style.display = 'none';
        }
    });
});