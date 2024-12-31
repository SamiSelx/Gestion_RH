document.addEventListener("DOMContentLoaded", function() {
    // Retrieve the stored click counts from localStorage (if available)
    const clickCounts = JSON.parse(localStorage.getItem('menuClicks')) || {};

    // Function to update the click count and check if item should be moved to "Favoris"
    function updateClickCount(menuId) {
        if (!clickCounts[menuId]) {
            clickCounts[menuId] = 0;
        }

        // Increment click count for this menu item
        clickCounts[menuId]++;
        
        // Store the updated click count in localStorage
        localStorage.setItem('menuClicks', JSON.stringify(clickCounts));

        console.log(`Item clicked: ${menuId}, Click count: ${clickCounts[menuId]}`); // Debugging line

        // If clicked more than 3 times, move the item to "Favoris"
        if (clickCounts[menuId] > 3) {
            moveToFavorites(menuId);
        }
    }

    // Function to move the item to "Favoris"
    function moveToFavorites(menuId) {
        const menuItem = document.querySelector(`li[data-id="${menuId}"]`);
        const favorisMenu = document.querySelector('.favoris .dropdown-menu');

        if (menuItem && favorisMenu) {
            // Check if the item is already in the "Favoris" menu
            if (!favorisMenu.querySelector(`li[data-id="${menuId}"]`)) {
                // Clone the item
                const clonedItem = menuItem.cloneNode(true);
                clonedItem.classList.add('favoris-item'); // Optional: style it differently

                // Append the cloned item to the "Favoris" dropdown
                favorisMenu.appendChild(clonedItem);

                // Optionally hide the original item from the main menu
                menuItem.style.display = 'none';

                console.log(`Item moved to Favoris: ${menuId}`); // Debugging line
            }
        }
    }

    // Add event listeners to each menu item
    document.querySelectorAll('.liste li').forEach(item => {
        item.addEventListener('click', function() {
            const menuId = item.getAttribute('data-id');
            updateClickCount(menuId);
        });
    });

    // Optional: Initialize any items that have been clicked more than 3 times
    Object.keys(clickCounts).forEach(menuId => {
        if (clickCounts[menuId] > 3) {
            moveToFavorites(menuId);
        }
    });
});
