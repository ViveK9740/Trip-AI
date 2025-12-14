import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import Home from './pages/Home';
import TripHistory from './pages/TripHistory';
import TripDetail from './pages/TripDetail';
import ProtectedRoute from './components/ProtectedRoute';
import ThemeToggle from './components/ThemeToggle';
import UserMenu from './components/UserMenu';
import './App.css';

function App() {
    return (
        <Router>
            <div className="app">
                <Routes>
                    {/* Public Landing Page */}
                    <Route path="/" element={<Landing />} />
                    
                    {/* Protected Routes */}
                    <Route path="/home" element={
                        <ProtectedRoute>
                            <ThemeToggle />
                            <div className="app-header">
                                <UserMenu />
                            </div>
                            <Home />
                        </ProtectedRoute>
                    } />
                    {/* Redirect dashboard to trips */}
                    <Route path="/dashboard" element={<Navigate to="/trips" replace />} />
                    <Route path="/trips" element={
                        <ProtectedRoute>
                            <ThemeToggle />
                            <div className="app-header">
                                <UserMenu />
                            </div>
                            <TripHistory />
                        </ProtectedRoute>
                    } />
                    <Route path="/trip/:tripId" element={
                        <ProtectedRoute>
                            <ThemeToggle />
                            <div className="app-header">
                                <UserMenu />
                            </div>
                            <TripDetail />
                        </ProtectedRoute>
                    } />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
