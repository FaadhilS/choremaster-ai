// API configuration
const API_BASE_URL = 'https://choremaster-ai.onrender.com';

// Helper function for API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Grocery functions
async function loadGroceries() {
    const data = await apiCall('/groceries');
    return data.items;
}

async function addGroceryItem(name, quantity = "1") {
    return await apiCall('/groceries', 'POST', { name, quantity });
}

async function deleteGroceryItem(itemId) {
    return await apiCall(`/groceries/${itemId}`, 'DELETE');
}

async function getGrocerySuggestions() {
    return await apiCall('/groceries/suggest', 'POST');
}

// Reminder functions
async function loadReminders() {
    const data = await apiCall('/reminders');
    return data.reminders;
}

async function addReminder(title, date, time) {
    return await apiCall('/reminders', 'POST', { title, date, time });
}

async function deleteReminder(reminderId) {
    return await apiCall(`/reminders/${reminderId}`, 'DELETE');
}

// Ride booking functions
async function bookRide(pickup, destination, service) {
    return await apiCall('/rides/book', 'POST', { pickup, destination, service });
}

async function getRecentRides() {
    const data = await apiCall('/rides/recent');
    return data.bookings;
}

// Dashboard functions
async function getDashboardStats() {
    return await apiCall('/dashboard/stats');
}

// Chat function
async function sendChatMessage(message) {
    return await apiCall('/chat', 'POST', { message });
}
