// frontend/js/auth.js
import axios from './api'; // Assuming api.js is in the same directory

async function login(username, password) {
    try {
        const response = await axios.post('/login/', { username, password });
        const token = response.data.token;
        localStorage.setItem('jwt_token', token);
        return true; // Login successful
    } catch (error) {
        console.error('Login error:', error);
        return false; // Login failed
    }
}
