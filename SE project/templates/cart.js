// cart.js

// Array to store selected items
var selectedItems = [];

// Function to add an item to the cart
function addItem(item) {
    selectedItems.push(item);
    updateCartDisplay();
}

// Function to remove an item from the cart
function removeItem(item) {
    var index = selectedItems.indexOf(item);
    if (index !== -1) {
        selectedItems.splice(index, 1);
    }
    updateCartDisplay();
}

// Function to update the cart display
function updateCartDisplay() {
    var cartItemsList = document.querySelector('.cart-items');
    cartItemsList.innerHTML = ''; // Clear the existing list
    selectedItems.forEach(function(item) {
        var listItem = document.createElement('li');
        listItem.textContent = item;
        cartItemsList.appendChild(listItem);
    });
}

// Function to toggle the visibility of the cart items
function toggleCart() {
    var cartItemsList = document.querySelector('.cart-items');
    cartItemsList.style.display = (cartItemsList.style.display === 'none') ? 'block' : 'none';
}

// Example usage
// Call addItem(itemName) when the + button is clicked
// Call removeItem(itemName) when the - button is clicked
