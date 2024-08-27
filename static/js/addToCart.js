document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');
    const addToCartModal = new bootstrap.Modal(document.getElementById('addToCartModal'));

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            addToCartModal.show();
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const addToCartModal = document.getElementById('addToCartModal');
    const addToCartForm = document.getElementById('addToCartForm');

    // Triggered when the modal is shown
    addToCartModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Button that triggered the modal
        const animalId = button.getAttribute('data-animal-id'); // Extract info from data-* attributes

        // Update the form action dynamically
        addToCartForm.action = `/cart/animal/add/${animalId}/`;
    });
});
