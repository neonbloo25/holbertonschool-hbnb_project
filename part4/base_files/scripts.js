// Helper to get cookie by name
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }
  
  // View details button redirect
  function viewDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
  }
  
  // Display places as cards
  function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = ''; // Clear the container before displaying new places
  
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.style.margin = '20px';
        card.style.padding = '10px';
        card.style.border = '1px solid #ddd';
        card.style.borderRadius = '10px';
  
        card.innerHTML = `
            <h3>${place.name}</h3>
            <p>Price per night: $${place.price_per_night}</p>
            <button class="details-button" onclick="viewDetails('${place.id}')">View Details</button>
        `;
        container.appendChild(card);
    });
  }
  
  // Filter displayed places by price
  function filterPlaces(priceLimit) {
    if (priceLimit === 'all') {
        displayPlaces(allPlaces); // Display all places if no filter is applied
        return;
    }
  
    const maxPrice = parseFloat(priceLimit);
    const filtered = allPlaces.filter(place => place.price_per_night <= maxPrice);
    displayPlaces(filtered); // Display filtered places
  }
  
  // Fetch all places from API
  let allPlaces = [];
  
  async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/places', {
            headers: {
                'Authorization': `Bearer ${token}` // Send the token for authentication
            }
        });
  
        if (response.ok) {
            const data = await response.json();
            allPlaces = data.places; // Store all places
            displayPlaces(allPlaces); // Display all places on the page
        } else {
            alert('Failed to fetch places. Are you logged in?');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
  }
  
  // Handle login form submission
  async function handleLogin(event) {
    event.preventDefault(); // Prevent form from refreshing the page
  
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
  
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`; // Store the token in a cookie
            window.location.href = 'index.html'; // Redirect to the main page after login
        } else {
            const errorMsg = await response.text();
            document.getElementById('error-message').innerText = `Login failed: ${errorMsg}`;
        }
    } catch (error) {
        console.error('Login error:', error);
        document.getElementById('error-message').innerText = 'An error occurred during login.';
    }
  }
  
  // DOM loaded – decide what page we’re on
  document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token'); // Get the authentication token from the cookie
  
    // If login form is present, handle the login submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
  
    // Handle the login link visibility based on token
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }
  
    // If places list is present and token is available, fetch places from API
    const placesList = document.getElementById('places-list');
    if (placesList && token) {
        fetchPlaces(token);
    }
  
    // Handle price filter change
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (e) => {
            filterPlaces(e.target.value);
        });
    }
  });
  