import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
    const [preferences, setPreferences] = useState(null);
    const [trips, setTrips] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchUserData();
    }, []);

    const fetchUserData = async () => {
        try {
            const token = localStorage.getItem('token');
            const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';
            
            // Fetch trips with authentication
            const tripsRes = await axios.get(`${API_BASE_URL}/api/trips`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            // Set default preferences for now (or remove this section if not needed)
            setPreferences({
                budget: 'mid_range',
                travelStyle: 'balanced'
            });
            setTrips(tripsRes.data || []);
        } catch (error) {
            console.error('Error fetching data:', error);
            setTrips([]);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="dashboard-loading">
                <div className="spinner"></div>
                <p>Loading your dashboard...</p>
            </div>
        );
    }

    return (
        <div className="dashboard-page">
            <header className="dashboard-header">
                <div className="container">
                    <div className="header-content">
                        <Link to="/" className="logo">
                            <span className="logo-icon">✈️</span>
                            <span className="logo-text gradient-text">TripAI</span>
                        </Link>
                        <Link to="/" className="btn btn-primary">
                            Plan New Trip
                        </Link>
                    </div>
                </div>
            </header>

            <main className="dashboard-main">
                <div className="container-wide">
                    <div className="dashboard-title">
                        <h1 className="gradient-text">Your Travel Dashboard</h1>
                        <p className="text-secondary">Manage your trips and preferences</p>
                    </div>

                    {/* Preferences Section */}
                    {preferences && (
                        <section className="preferences-section">
                            <div className="section-card card">
                                <h2>🎯 Your Preferences</h2>
                                <div className="preferences-grid">
                                    <div className="pref-category">
                                        <h3>Dietary</h3>
                                        <div className="tags">
                                            {preferences.dietary.length > 0 ? (
                                                preferences.dietary.map((item, index) => (
                                                    <span key={index} className="tag">{item}</span>
                                                ))
                                            ) : (
                                                <span className="text-muted">No preferences set</span>
                                            )}
                                        </div>
                                    </div>

                                    <div className="pref-category">
                                        <h3>Activities</h3>
                                        <div className="tags">
                                            {preferences.activities.length > 0 ? (
                                                preferences.activities.map((item, index) => (
                                                    <span key={index} className="tag">{item}</span>
                                                ))
                                            ) : (
                                                <span className="text-muted">No preferences set</span>
                                            )}
                                        </div>
                                    </div>

                                    <div className="pref-category">
                                        <h3>Budget Range</h3>
                                        <p className="budget-range">
                                            ₹{preferences.budgetRange.min.toLocaleString()} - ₹{preferences.budgetRange.max.toLocaleString()}
                                        </p>
                                    </div>

                                    <div className="pref-category">
                                        <h3>Travel Style</h3>
                                        <span className="tag primary">{preferences.travelStyle}</span>
                                    </div>
                                </div>
                            </div>
                        </section>
                    )}

                    {/* Trip History */}
                    <section className="trips-section">
                        <h2>📚 Trip History</h2>

                        {trips.length > 0 ? (
                            <div className="trips-grid">
                                {trips.map((trip) => (
                                    <div key={trip._id} className="trip-card card">
                                        <div className="trip-header">
                                            <div className="trip-destination">
                                                <h3>{trip.destination}</h3>
                                                <div className="trip-meta">
                                                    <span>{trip.duration.days} days</span>
                                                    <span>•</span>
                                                    <span>₹{trip.budget.toLocaleString()}</span>
                                                </div>
                                            </div>
                                            <span className={`status-badge ${trip.status}`}>
                                                {trip.status}
                                            </span>
                                        </div>

                                        <p className="trip-query">{trip.userQuery}</p>

                                        <div className="trip-stats">
                                            <div className="stat">
                                                <span className="stat-label">Activities</span>
                                                <span className="stat-value">
                                                    {trip.itinerary.reduce((sum, day) => sum + day.activities.length, 0)}
                                                </span>
                                            </div>
                                            <div className="stat">
                                                <span className="stat-label">Days</span>
                                                <span className="stat-value">{trip.duration.days}</span>
                                            </div>
                                            <div className="stat">
                                                <span className="stat-label">Total Cost</span>
                                                <span className="stat-value">
                                                    ₹{trip.budgetBreakdown.total.toLocaleString()}
                                                </span>
                                            </div>
                                        </div>

                                        <div className="trip-preferences">
                                            {trip.preferences.dietary.map((item, idx) => (
                                                <span key={idx} className="mini-tag">{item}</span>
                                            ))}
                                            {trip.preferences.activities.map((item, idx) => (
                                                <span key={idx} className="mini-tag">{item}</span>
                                            ))}
                                        </div>

                                        <div className="trip-date">
                                            Created {new Date(trip.createdAt).toLocaleDateString('en-US', {
                                                month: 'short',
                                                day: 'numeric',
                                                year: 'numeric'
                                            })}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="empty-state card-glass">
                                <span className="empty-icon">🧳</span>
                                <h3>No trips yet</h3>
                                <p className="text-muted">Start planning your first adventure!</p>
                                <Link to="/" className="btn btn-primary mt-md">
                                    Plan a Trip
                                </Link>
                            </div>
                        )}
                    </section>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
