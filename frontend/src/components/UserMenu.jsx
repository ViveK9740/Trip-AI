import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import Login from './Login';
import Signup from './Signup';
import './UserMenu.css';

const UserMenu = () => {
    const { user, logout, isAuthenticated } = useAuth();
    const [showLogin, setShowLogin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);
    const [showDropdown, setShowDropdown] = useState(false);

    console.log('UserMenu Render:', { isAuthenticated, user, showLogin, showSignup });

    const handleSwitchToSignup = () => {
        console.log('Switching to Signup');
        setShowLogin(false);
        setShowSignup(true);
    };

    const handleSwitchToLogin = () => {
        console.log('Switching to Login');
        setShowSignup(false);
        setShowLogin(true);
    };

    const handleLoginClick = () => {
        console.log('Login clicked');
        setShowLogin(true);
    };

    const handleSignupClick = () => {
        console.log('Signup clicked');
        setShowSignup(true);
    };

    if (!isAuthenticated) {
        return (
            <>
                <div className="user-menu-guest">
                    <button className="btn btn-secondary" onClick={handleLoginClick}>
                        Log In
                    </button>
                    <button className="btn btn-primary" onClick={handleSignupClick}>
                        Sign Up
                    </button>
                </div>

                {showLogin && (
                    <Login
                        onClose={() => setShowLogin(false)}
                        onSwitchToSignup={handleSwitchToSignup}
                    />
                )}
                {showSignup && (
                    <Signup
                        onClose={() => setShowSignup(false)}
                        onSwitchToLogin={handleSwitchToLogin}
                    />
                )}
            </>
        );
    }

    return (
        <div className="user-menu">
            <button
                className="user-menu-button"
                onClick={() => setShowDropdown(!showDropdown)}
            >
                <div className="user-avatar">
                    {user?.name?.charAt(0).toUpperCase() || 'U'}
                </div>
                <span className="user-name">{user?.name || 'User'}</span>
            </button>

            {showDropdown && (
                <>
                    <div className="dropdown-overlay" onClick={() => setShowDropdown(false)} />
                    <div className="user-dropdown">
                        <div className="dropdown-header">
                            <div className="user-info">
                                <p className="user-info-name">{user?.name}</p>
                                <p className="user-info-email">{user?.email}</p>
                            </div>
                        </div>
                        <div className="dropdown-divider" />
                        <a href="/trips" className="dropdown-item">
                            📚 My Trips
                        </a>
                        <button className="dropdown-item" onClick={() => { logout(); setShowDropdown(false); }}>
                            🚪 Logout
                        </button>
                    </div>
                </>
            )}
        </div>
    );
};

export default UserMenu;
