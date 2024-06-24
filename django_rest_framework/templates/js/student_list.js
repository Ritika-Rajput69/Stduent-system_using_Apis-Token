// frontend/js/components/studentsList.js
import React, { useState, useEffect } from 'react';
import api from '../api';

const studentsList = () => {
    const [students, setstudents] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.get('/students/');
                setstudents(response.data);
            } catch (error) {
                console.error('Error fetching students:', error);
            }
        };
        fetchData();
    }, []);

    // ... render students list
};

export default studentsList;

// frontend/js/components/studentsForm.js
import React, { useState } from 'react';
import api from '../api';

const studentsForm = () => {
    const [name, setName] = useState('');
    // ... other students data fields

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/students/', { name, // ... other data });
            console.log('students created:', response.data);
            // Handle successful creation (e.g., clear form, refresh list)
        } catch (error) {
            console.error('Error creating students:', error);
            // Handle errors (e.g., display error message)
        }
    };

    return (
        <form onSubmit={handleSubmit}>)

