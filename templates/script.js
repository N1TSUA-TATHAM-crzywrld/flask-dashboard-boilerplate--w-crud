// script.js

// Function to toggle profile edit form visibility
function editProfile() {
    document.querySelector('.profile-container').style.display = 'none';
    document.querySelector('#edit-container').style.display = 'block';
}

// Function to cancel profile edit and return to view
function cancelEdit() {
    document.querySelector('.profile-container').style.display = 'block';
    document.querySelector('#edit-container').style.display = 'none';
}

// Function to handle form submission (saving changes)
function updateProfile(event) {
    event.preventDefault(); // Prevent form submission and page reload

    const name = document.getElementById('edit-name').value;
    const email = document.getElementById('edit-email').value;
    const phone = document.getElementById('edit-phone').value;
    const address = document.getElementById('edit-address').value;

    // Update profile info on the page
    document.getElementById('name').textContent = name;
    document.getElementById('email').textContent = email;
    document.getElementById('phone').textContent = phone;
    document.getElementById('address').textContent = address;

    // Hide the edit form and return to the profile view
    cancelEdit();
}
