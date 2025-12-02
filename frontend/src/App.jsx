import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import TripHistory from './pages/TripHistory';
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
                    <Route path="/dashboard" element={
                        <ProtectedRoute>
                            <ThemeToggle />
                            <div className="app-header">
                                <UserMenu />
                            </div>
                            <Dashboard />
                        </ProtectedRoute>
                    } />
                    <Route path="/trips" element={
                        <ProtectedRoute>
                            <ThemeToggle />
                            <div className="app-header">
                                <UserMenu />
                            </div>
                            <TripHistory />
                        </ProtectedRoute>
                    } />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
