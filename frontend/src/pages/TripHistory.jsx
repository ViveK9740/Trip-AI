import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import './TripHistory.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

const TripHistory = () => {
    const { isAuthenticated, user } = useAuth();
    const [trips, setTrips] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (isAuthenticated) {
            fetchTrips();
        }
    }, [isAuthenticated]);

    const fetchTrips = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/trips`);
            setTrips(response.data);
        } catch (err) {
            setError('Failed to load trips');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const deleteTrip = async (tripId) => {
        if (!confirm('Are you sure you want to delete this trip?')) return;

        try {
            await axios.delete(`${API_BASE_URL}/api/trips/${tripId}`);
            setTrips(trips.filter(trip => trip.id !== tripId));
        } catch (err) {
            alert('Failed to delete trip');
            console.error(err);
        }
    };

    if (!isAuthenticated) {
        return (
            <div className="trip-history-page">
                <div className="empty-state">
                    <h2>Please log in to view your trips</h2>
                    <p>Sign up or log in to save and access your travel itineraries</p>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="trip-history-page">
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Loading your trips...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="trip-history-page">
            <div className="container">
                <header className="trip-history-header">
                    <h1 className="gradient-text">My Trips</h1>
                    <p className="trip-history-subtitle">
                        {trips.length} saved {trips.length === 1 ? 'trip' : 'trips'}
                    </p>
                </header>

                {error && <div className="error-message">{error}</div>}

                {trips.length === 0 ? (
                    <div className="empty-state">
                        <div className="empty-icon">✈️</div>
                        <h2>No trips saved yet</h2>
                        <p>Start planning your next adventure and save your itineraries here!</p>
                        <a href="/" className="btn btn-primary">
                            Plan New Trip
                        </a>
                    </div>
                ) : (
                    <div className="trips-grid">
                        {trips.map(trip => (
                            <div key={trip.id} className="trip-card">
                                <div className="trip-card-header">
                                    <h3>{trip.destination}</h3>
                                    <button
                                        className="trip-delete-btn"
                                        onClick={() => deleteTrip(trip.id)}
                                        title="Delete trip"
                                    >
                                        🗑️
                                    </button>
                                </div>

                                <div className="trip-card-meta">
                                    <span className="trip-duration">📅 {trip.days} days</span>
                                    {trip.budget && (
                                        <span className="trip-budget">💰 ₹{trip.budget.toLocaleString()}</span>
                                    )}
                                </div>

                                {trip.start_date && (
                                    <p className="trip-dates">
                                        {new Date(trip.start_date).toLocaleDateString()} -
                                        {trip.end_date && ` ${new Date(trip.end_date).toLocaleDateString()}`}
                                    </p>
                                )}

                                <p className="trip-saved-date">
                                    Saved {new Date(trip.created_at).toLocaleDateString()}
                                </p>

                                <a href={`/trip/${trip.id}`} className="btn btn-secondary trip-view-btn">
                                    View Itinerary
                                </a>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default TripHistory;
