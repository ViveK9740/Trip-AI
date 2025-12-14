import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import ItineraryDisplay from '../components/ItineraryDisplay';
import './TripDetail.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

const TripDetail = () => {
    const { tripId } = useParams();
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const [trip, setTrip] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (isAuthenticated && tripId) {
            fetchTripDetails();
        }
    }, [isAuthenticated, tripId]);

    const fetchTripDetails = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_BASE_URL}/api/trips/${tripId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            setTrip(response.data);
        } catch (err) {
            setError('Failed to load trip details');
            console.error('Fetch trip error:', err);
        } finally {
            setLoading(false);
        }
    };

    if (!isAuthenticated) {
        return (
            <div className="trip-detail-page">
                <div className="empty-state">
                    <h2>Please log in to view this trip</h2>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="trip-detail-page">
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Loading trip details...</p>
                </div>
            </div>
        );
    }

    if (error || !trip) {
        return (
            <div className="trip-detail-page">
                <div className="container">
                    <div className="error-message">{error || 'Trip not found'}</div>
                    <button onClick={() => navigate('/trips')} className="btn btn-primary">
                        ← Back to My Trips
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="trip-detail-page">
            <div className="container">
                <div className="trip-detail-header">
                    <button onClick={() => navigate('/trips')} className="btn btn-secondary back-btn">
                        ← Back to My Trips
                    </button>
                    <div className="trip-meta">
                        <span className="trip-saved">Saved on {new Date(trip.created_at).toLocaleDateString()}</span>
                    </div>
                </div>

                {trip.itinerary_data && trip.itinerary_data.itinerary && (
                    <ItineraryDisplay
                        itinerary={trip.itinerary_data.itinerary}
                        budgetValidation={trip.itinerary_data.budgetValidation}
                        destination={trip.destination}
                        tripDetails={{
                            destination: trip.destination,
                            days: trip.days,
                            budget: trip.budget
                        }}
                    />
                )}
            </div>
        </div>
    );
};

export default TripDetail;
