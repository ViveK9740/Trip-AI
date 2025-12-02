import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ChatInterface from '../components/ChatInterface';
import ItineraryDisplay from '../components/ItineraryDisplay';
import './Home.css';

const Home = () => {
    const [planData, setPlanData] = useState(null);

    const handlePlanCreated = (data) => {
        setPlanData(data);

        // Smooth scroll to itinerary
        setTimeout(() => {
            document.getElementById('itinerary-section')?.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }, 300);
    };

    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-background">
                    <div className="gradient-orb orb-1"></div>
                    <div className="gradient-orb orb-2"></div>
                    <div className="gradient-orb orb-3"></div>
                </div>

                <div className="container hero-content">
                    <div className="logo">
                        <span className="logo-icon">✈️</span>
                        <span className="logo-text gradient-text">TripAI</span>
                    </div>

                    <h1 className="hero-title animate-fadeInUp">
                        Your Intelligent <span className="gradient-text">Travel Companion</span>
                    </h1>

                    <p className="hero-subtitle animate-fadeInUp" style={{ animationDelay: '0.1s' }}>
                        Experience the future of travel planning. Just tell us your dream trip, and our AI agents
                        will craft the perfect itinerary tailored to your preferences and budget.
                    </p>

                    <div className="features-grid animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
                        <div className="feature-card card-glass">
                            <div className="feature-icon">🤖</div>
                            <h3>AI-Powered</h3>
                            <p>Advanced agents understand your needs and create personalized plans</p>
                        </div>
                        <div className="feature-card card-glass">
                            <div className="feature-icon">⚡</div>
                            <h3>Instant Planning</h3>
                            <p>Get comprehensive itineraries in seconds, not hours</p>
                        </div>
                        <div className="feature-card card-glass">
                            <div className="feature-icon">💰</div>
                            <h3>Budget Smart</h3>
                            <p>Stay within your budget with intelligent cost optimization</p>
                        </div>
                        <div className="feature-card card-glass">
                            <div className="feature-icon">🌟</div>
                            <h3>Personalized</h3>
                            <p>Learns your preferences for even better future recommendations</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Chat Section */}
            <section className="chat-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="gradient-text">Start Planning Your Adventure</h2>
                        <p className="text-secondary">
                            Just describe your trip in natural language. For example:
                        </p>
                    </div>

                    <div className="example-queries">
                        <div className="example-chip">"3-day weekend trip to Goa, under ₹15,000, beaches and veg food"</div>
                        <div className="example-chip">"5-day honeymoon in Kerala, ₹50,000, romantic and scenic"</div>
                        <div className="example-chip">"Week-long trek in Himachal, budget-friendly, adventure activities"</div>
                    </div>

                    <div className="chat-container animate-fadeIn">
                        <ChatInterface onPlanCreated={handlePlanCreated} />
                    </div>

                    <div className="quick-links">
                        <Link to="/dashboard" className="btn btn-secondary">
                            View Past Trips
                        </Link>
                    </div>
                </div>
            </section>

            {/* Itinerary Section */}
            {planData && (
                <section id="itinerary-section" className="itinerary-section">
                    <div className="container-wide">
                        <ItineraryDisplay
                            itinerary={planData.itinerary}
                            budgetValidation={planData.budgetValidation}
                            destination={planData.destination}
                        />
                    </div>
                </section>
            )}

            {/* Footer */}
            <footer className="footer">
                <div className="container">
                    <div className="footer-content">
                        <div className="footer-brand">
                            <div className="logo">
                                <span className="logo-icon">✈️</span>
                                <span className="logo-text gradient-text">TripAI</span>
                            </div>
                            <p className="text-muted">
                                Agentic AI-powered travel planning for the modern explorer
                            </p>
                        </div>
                        <div className="footer-info">
                            <p className="text-muted">
                                Powered by 🤖 Google Gemini AI • 🗺️ Mappls API • 🍃 MongoDB Atlas
                            </p>
                            <p className="text-muted">
                                © 2025 TripAI. Made with ❤️ for travelers everywhere.
                            </p>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Home;
