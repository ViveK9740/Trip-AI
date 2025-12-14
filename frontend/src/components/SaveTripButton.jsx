import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import Login from './Login';
import Signup from './Signup';
import './SaveTripButton.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

const SaveTripButton = ({ itinerary, tripDetails }) => {
    const { isAuthenticated } = useAuth();
    const [showLogin, setShowLogin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);

    const handleSave = async () => {
        if (!isAuthenticated) {
            setShowSignup(true);
            return;
        }

        setSaving(true);
        try {
            const token = localStorage.getItem('token');
            
            // Prepare trip data matching backend schema
            const tripData = {
                destination: tripDetails.destination || 'My Trip',
                start_date: tripDetails.start_date || tripDetails.startDate || null,
                end_date: tripDetails.end_date || tripDetails.endDate || null,
                days: parseInt(tripDetails.days) || 3,
                budget: tripDetails.budget ? parseFloat(tripDetails.budget) : null,
                itinerary_data: {
                    itinerary: itinerary,
                    budgetValidation: tripDetails.budgetValidation || {}
                }
            };
            
            await axios.post(`${API_BASE_URL}/api/trips`, tripData, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            setSaved(true);
            setTimeout(() => setSaved(false), 3000);
        } catch (error) {
            console.error('Failed to save trip:', error);
            alert('Failed to save trip. Please try again.');
        } finally {
            setSaving(false);
        }
    };

    return (
        <>
            <button
                className={`btn btn-primary save-trip-btn ${saved ? 'saved' : ''}`}
                onClick={handleSave}
                disabled={saving || saved}
            >
                {saved ? '✓ Saved!' : saving ? 'Saving...' : '💾 Save Trip'}
            </button>

            {showLogin && (
                <Login
                    onClose={() => setShowLogin(false)}
                    onSwitchToSignup={() => { setShowLogin(false); setShowSignup(true); }}
                />
            )}
            {showSignup && (
                <Signup
                    onClose={() => setShowSignup(false)}
                    onSwitchToLogin={() => { setShowSignup(false); setShowLogin(true); }}
                />
            )}
        </>
    );
};

export default SaveTripButton;
