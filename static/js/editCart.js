document.addEventListener('DOMContentLoaded', function() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');

    // Handle quantity increase and decrease
    cartItems.addEventListener('click', function(event) {
        const target = event.target;
        if (target.classList.contains('quantity-increase') || target.classList.contains('quantity-decrease')) {
            const cartItem = target.closest('.cart-item');
            const item_id = cartItem.dataset.itemId;
            const action = target.classList.contains('quantity-increase') ? 'increase' : 'decrease';

            updateCartItemQuantity(item_id, action, cartItem);
        }
    });





    // Handle age and sex change
    cartItems.addEventListener('change', function(event) {
        const target = event.target;
        if (target.name === 'age' || target.name === 'sex') {
            const cartItem = target.closest('.cart-item');
            const item_id = cartItem.dataset.itemId;
            const age = cartItem.querySelector('select[name="age"]').value;
            const sex = cartItem.querySelector('select[name="sex"]').value;

            updateCartItemDetails(item_id, age, sex, cartItem);
        }
    });



    // Handle cart item removal
    cartItems.addEventListener('click', function(event) {
        const target = event.target;
        if (target.classList.contains('cart-item-remove')) {
            const cartItem = target.closest('.cart-item');
            const item_id = cartItem.dataset.itemId;

            removeCartItem(item_id, cartItem);
        }
    });






    function updateCartItemQuantity(item_id, action, cartItem) {
        fetch(`/update-cart-item-quantity/${item_id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `action=${action}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.quantity !== undefined) {
                const quantityInput = cartItem.querySelector('.quantity-input');
                quantityInput.value = data.quantity;

                // Convert total_price and cart_total to numbers
                const totalPrice = parseFloat(data.total_price); // Convert to float
                const cartTotal = parseFloat(data.cart_total); // Convert to float

                const priceDisplay = cartItem.querySelector('.cart-item-price');
                priceDisplay.innerText = `$${totalPrice.toFixed(2)}`; // Display formatted price

                updateCartTotal(cartTotal); // Pass the total as a number
            } else {
                console.error('Failed to update quantity:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    }







    function updateCartItemDetails(item_id, age, sex, cartItem) {
        fetch(`/update-cart-item-details/${item_id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `age=${age}&sex=${sex}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.total_price !== undefined) {
                cartItem.querySelector('.cart-item-price').innerText = `$${data.total_price.toFixed(2)}`;
                updateCartTotal(data.cart_total);
            } else {
                console.error('Failed to update age/sex:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    }




    function removeCartItem(item_id, cartItem) {
        fetch(`/remove-cart-item/${item_id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Check if the item was successfully removed
            if (data.item_removed) {
                // Remove the cart item from the DOM
                cartItem.remove();

                // Update the total price in the cart
                const cartTotalValue = parseFloat(data.cart_total); // Convert to float
                updateCartTotal(cartTotalValue); // Update cart total dynamically

                // Check if the cart is empty and update the message
                if (data.cart_is_empty) {
                    cartItems.innerHTML = '<p>Your cart is empty.</p>'; // Display empty cart message
                }
            } else {
                console.error('Failed to remove item:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    }







    function updateCartTotal(total) {
        cartTotal.innerText = total.toFixed(2);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});