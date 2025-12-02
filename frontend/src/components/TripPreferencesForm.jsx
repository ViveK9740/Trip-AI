import React, { useState } from 'react';
import './TripPreferencesForm.css';

const TripPreferencesForm = ({ onSubmit, onClose }) => {
    const [formData, setFormData] = useState({
        destination: '',
        origin: '', // New field
        isRoundTrip: false, // New field
        duration: 3,
        travelers: {
            adults: 2,
            children: 0
        },
        budget: 50000,
        preferences: {
            dietary: [],
            transport_mode: 'public',
            accommodation_type: 'mid_range',
            travel_style: 'balanced',
            night_travel: false
        }
    });

    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handlePreferenceChange = (category, value) => {
        setFormData(prev => ({
            ...prev,
            preferences: {
                ...prev.preferences,
                [category]: value
            }
        }));
    };

    const handleCheckboxChange = (e) => {
        const { name, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: checked
        }));
    };

    const handleTravelerChange = (type, value) => {
        setFormData(prev => ({
            ...prev,
            travelers: {
                ...prev.travelers,
                [type]: parseInt(value) || 0
            }
        }));
    };

    const validateForm = () => {
        const newErrors = {};
        if (!formData.destination.trim()) newErrors.destination = 'Destination is required';
        if (!formData.origin.trim()) newErrors.origin = 'Starting point is required';
        if (formData.duration < 1) newErrors.duration = 'Duration must be at least 1 day';
        if (formData.budget < 1000) newErrors.budget = 'Budget seems too low';

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (validateForm()) {
            onSubmit(formData);
        }
    };

    return (
        <div className="trip-form-overlay">
            <div className="trip-form-container">
                <div className="form-header">
                    <h2>Plan Your Perfect Trip</h2>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                <form onSubmit={handleSubmit} className="trip-form">
                    {/* Basic Details Section */}
                    <div className="form-section">
                        <h3>📍 Where & When</h3>
                        <div className="form-row">
                            <div className="form-group">
                                <label>Starting Point (Origin)</label>
                                <input
                                    type="text"
                                    name="origin"
                                    value={formData.origin}
                                    onChange={handleChange}
                                    placeholder="e.g., Bengaluru"
                                    className={errors.origin ? 'error' : ''}
                                />
                                {errors.origin && <span className="error-msg">{errors.origin}</span>}
                            </div>

                            <div className="form-group">
                                <label>Destination</label>
                                <input
                                    type="text"
                                    name="destination"
                                    value={formData.destination}
                                    onChange={handleChange}
                                    placeholder="e.g., Goa"
                                    className={errors.destination ? 'error' : ''}
                                />
                                {errors.destination && <span className="error-msg">{errors.destination}</span>}
                            </div>
                        </div>

                        <div className="form-row">
                            <div className="form-group checkbox-group">
                                <label className="checkbox-label">
                                    <input
                                        type="checkbox"
                                        name="isRoundTrip"
                                        checked={formData.isRoundTrip}
                                        onChange={handleCheckboxChange}
                                    />
                                    🔄 Round Trip (Return to Origin)
                                </label>
                            </div>
                        </div>

                        <div className="form-row">
                            <div className="form-group">
                                <label>Duration (Days)</label>
                                <input
                                    type="number"
                                    name="duration"
                                    value={formData.duration}
                                    onChange={handleChange}
                                    min="1"
                                    max="30"
                                />
                            </div>
                            <div className="form-group">
                                <label>Budget (₹)</label>
                                <input
                                    type="number"
                                    name="budget"
                                    value={formData.budget}
                                    onChange={handleChange}
                                    step="1000"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Travelers Section */}
                    <div className="form-section">
                        <h3>👥 Travelers</h3>
                        <div className="form-row">
                            <div className="form-group">
                                <label>Adults</label>
                                <input
                                    type="number"
                                    value={formData.travelers.adults}
                                    onChange={(e) => handleTravelerChange('adults', e.target.value)}
                                    min="1"
                                />
                            </div>
                            <div className="form-group">
                                <label>Children</label>
                                <input
                                    type="number"
                                    value={formData.travelers.children}
                                    onChange={(e) => handleTravelerChange('children', e.target.value)}
                                    min="0"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Preferences Section */}
                    <div className="form-section">
                        <h3>✨ Preferences</h3>

                        <div className="form-group">
                            <label>Travel Style</label>
                            <div className="radio-group">
                                {['relaxed', 'balanced', 'adventure', 'cultural'].map(style => (
                                    <label key={style} className={`radio-card ${formData.preferences.travel_style === style ? 'selected' : ''}`}>
                                        <input
                                            type="radio"
                                            name="travel_style"
                                            value={style}
                                            checked={formData.preferences.travel_style === style}
                                            onChange={(e) => handlePreferenceChange('travel_style', e.target.value)}
                                        />
                                        <span className="radio-label">{style.charAt(0).toUpperCase() + style.slice(1)}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        <div className="form-group">
                            <label>Accommodation Type</label>
                            <select
                                value={formData.preferences.accommodation_type}
                                onChange={(e) => handlePreferenceChange('accommodation_type', e.target.value)}
                            >
                                <option value="budget">Budget (Hostels/Homestays)</option>
                                <option value="mid_range">Mid-Range (3-4 Star Hotels)</option>
                                <option value="luxury">Luxury (5 Star/Resorts)</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Transport Mode</label>
                            <select
                                value={formData.preferences.transport_mode}
                                onChange={(e) => handlePreferenceChange('transport_mode', e.target.value)}
                            >
                                <option value="public">Public Transport (Bus/Train)</option>
                                <option value="own_vehicle">Own Vehicle</option>
                                <option value="rental">Rental Car/Bike</option>
                                <option value="flight">Flight</option>
                            </select>
                        </div>

                        <div className="form-group checkbox-group">
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    checked={formData.preferences.night_travel}
                                    onChange={(e) => handlePreferenceChange('night_travel', e.target.checked)}
                                />
                                🌙 Night Travel Preferred
                            </label>
                        </div>
                    </div>

                    <div className="form-actions">
                        <button type="button" className="cancel-btn" onClick={onClose}>Cancel</button>
                        <button type="submit" className="submit-btn">🚀 Generate Itinerary</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default TripPreferencesForm;
