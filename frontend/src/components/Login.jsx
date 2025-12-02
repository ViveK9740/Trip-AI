import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

const Login = ({ onClose, onSuccess, onSwitchToSignup }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const result = await login(email, password);

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
            <h2 className="gradient-text">Welcome Back</h2>
            <p className="auth-subtitle">Log in to save and view your trips</p>

            <form onSubmit={handleSubmit} className="auth-form">
                {error && <div className="auth-error">{error}</div>}

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
                        placeholder="••••••••"
                        className="input"
                    />
                </div>

                <button
                    type="submit"
                    className="btn btn-primary auth-submit-btn"
                    disabled={loading}
                >
                    {loading ? 'Logging in...' : 'Log In'}
                </button>
            </form>

            <div className="auth-footer">
                <p>Don't have an account?</p>
                <button className="auth-link-btn" onClick={onSwitchToSignup}>
                    Sign up
                </button>
            </div>
        </div>
    );
};

export default Login;
