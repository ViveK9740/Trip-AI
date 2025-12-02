import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

const Signup = ({ onClose, onSuccess, onSwitchToLogin }) => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { signup } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Validation
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        setLoading(true);
        const result = await signup(email, password, name);

        if (result.success) {
            if (onSuccess) onSuccess();
            if (onClose) onClose();
            navigate('/home');
        } else {
            setError(result.error);
        }

        setLoading(false);
    };

    return (
        <div className="auth-content">
            <h2 className="gradient-text">Create Account</h2>
            <p className="auth-subtitle">Start planning your perfect trip</p>

            <form onSubmit={handleSubmit} className="auth-form">
                {error && <div className="auth-error">{error}</div>}

                <div className="form-group">
                    <label>Name</label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        placeholder="John Doe"
                        className="input"
                    />
                </div>

                <div className="form-group">
                    <label>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        placeholder="your@email.com"
                        className="input"
                    />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        placeholder="Minimum 6 characters"
                        className="input"
                    />
                </div>

                <div className="form-group">
                    <label>Confirm Password</label>
                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                        placeholder="Re-enter password"
                        className="input"
                    />
                </div>

                <button
                    type="submit"
                    className="btn btn-primary auth-submit-btn"
                    disabled={loading}
                >
                    {loading ? 'Creating account...' : 'Sign Up'}
                </button>
            </form>

            <div className="auth-footer">
                <p>Already have an account?</p>
                <button className="auth-link-btn" onClick={onSwitchToLogin}>
                    Log in
                </button>
            </div>
        </div>
    );
};

export default Signup;
