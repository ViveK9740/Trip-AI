import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Login from '../components/Login';
import Signup from '../components/Signup';
import './Landing.css';

const Landing = () => {
    const [showAuth, setShowAuth] = useState(false);
    const [authMode, setAuthMode] = useState('login'); // 'login' or 'signup'
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();

    // Redirect if already authenticated
    React.useEffect(() => {
        if (isAuthenticated) {
            navigate('/home');
        }
    }, [isAuthenticated, navigate]);

    const openAuth = (mode) => {
        setAuthMode(mode);
        setShowAuth(true);
    };

    const closeAuth = () => {
        setShowAuth(false);
    };

    const switchAuthMode = () => {
        setAuthMode(authMode === 'login' ? 'signup' : 'login');
    };

    return (
        <div className="landing-page">
            {/* Animated Background */}
            <div className="landing-background">
                <div className="gradient-orb orb-1"></div>
                <div className="gradient-orb orb-2"></div>
                <div className="gradient-orb orb-3"></div>
                <div className="gradient-orb orb-4"></div>
            </div>

            {/* Navigation */}
            <nav className="landing-nav">
                <div className="container">
                    <div className="nav-content">
                        <div className="logo">
                            <span className="logo-icon">✈️</span>
                            <span className="logo-text gradient-text">TripAI</span>
                        </div>
                        <div className="nav-actions">
                            <button 
                                className="btn-ghost" 
                                onClick={() => openAuth('login')}
                            >
                                Sign In
                            </button>
                            <button 
                                className="btn-primary" 
                                onClick={() => openAuth('signup')}
                            >
                                Get Started
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="landing-hero">
                <div className="container">
                    <div className="hero-content">
                        <h1 className="hero-title">
                            Your Intelligent
                            <span className="gradient-text"> Travel Companion</span>
                        </h1>
                        <p className="hero-subtitle">
                            Experience the future of travel planning powered by AI. 
                            Just tell us your dream trip, and our intelligent agents 
                            will craft the perfect itinerary tailored to your preferences and budget.
                        </p>
                        <div className="hero-cta">
                            <button 
                                className="btn-hero" 
                                onClick={() => openAuth('signup')}
                            >
                                Start Planning Now
                                <span className="btn-icon">→</span>
                            </button>
                            <p className="cta-note">Free to use • No credit card required</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="landing-features">
                <div className="container">
                    <h2 className="section-title">Why Choose TripAI?</h2>
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="feature-icon">🤖</div>
                            <h3>AI-Powered Planning</h3>
                            <p>Advanced AI agents understand your needs and create personalized travel plans in seconds</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">💰</div>
                            <h3>Budget Optimization</h3>
                            <p>Smart budget management with realistic pricing and money-saving tips for every trip</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">🗺️</div>
                            <h3>Real Place Data</h3>
                            <p>Powered by Mappls API for accurate locations, attractions, and local recommendations</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">🎯</div>
                            <h3>Smart Route Planning</h3>
                            <p>Geographic clustering and optimization ensures efficient travel between attractions</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">⚙️</div>
                            <h3>Fully Customizable</h3>
                            <p>Choose your travel style, accommodation, transport mode, and dietary preferences</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">📱</div>
                            <h3>Easy to Use</h3>
                            <p>Simple chat interface - just describe your trip and let AI handle the rest</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="landing-how">
                <div className="container">
                    <h2 className="section-title">How It Works</h2>
                    <div className="steps-container">
                        <div className="step-card">
                            <div className="step-number">1</div>
                            <h3>Sign Up</h3>
                            <p>Create your free account in seconds</p>
                        </div>
                        <div className="step-arrow">→</div>
                        <div className="step-card">
                            <div className="step-number">2</div>
                            <h3>Describe Your Trip</h3>
                            <p>Tell us your destination, budget, and preferences</p>
                        </div>
                        <div className="step-arrow">→</div>
                        <div className="step-card">
                            <div className="step-number">3</div>
                            <h3>Get Your Itinerary</h3>
                            <p>Receive a detailed day-wise plan with real places</p>
                        </div>
                        <div className="step-arrow">→</div>
                        <div className="step-card">
                            <div className="step-number">4</div>
                            <h3>Start Your Journey</h3>
                            <p>Save, share, and explore with confidence</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="landing-cta">
                <div className="container">
                    <div className="cta-content">
                        <h2>Ready to Plan Your Next Adventure?</h2>
                        <p>Join thousands of travelers using AI to create perfect trips</p>
                        <button 
                            className="btn-hero" 
                            onClick={() => openAuth('signup')}
                        >
                            Get Started Free
                            <span className="btn-icon">→</span>
                        </button>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="landing-footer">
                <div className="container">
                    <div className="footer-content">
                        <div className="footer-brand">
                            <div className="logo">
                                <span className="logo-icon">✈️</span>
                                <span className="logo-text gradient-text">TripAI</span>
                            </div>
                            <p>Agentic AI-powered travel planning for the modern explorer</p>
                        </div>
                        <div className="footer-info">
                            <p>Powered by 🤖 Google Gemini AI • 🗺️ Mappls API • 🍃 MongoDB Atlas</p>
                            <p>© 2025 TripAI. Made with ❤️ for travelers everywhere.</p>
                        </div>
                    </div>
                </div>
            </footer>

            {/* Auth Modal */}
            {showAuth && (
                <div className="auth-overlay" onClick={closeAuth}>
                    <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
                        <button className="modal-close" onClick={closeAuth}>×</button>
                        {authMode === 'login' ? (
                            <Login onSuccess={closeAuth} onSwitchToSignup={switchAuthMode} />
                        ) : (
                            <Signup onSuccess={closeAuth} onSwitchToLogin={switchAuthMode} />
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Landing;
