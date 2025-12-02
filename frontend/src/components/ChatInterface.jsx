import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';
import TripPreferencesForm from './TripPreferencesForm';

const ChatInterface = ({ onPlanCreated }) => {
    const [inputMode, setInputMode] = useState('simple'); // 'simple' or 'detailed'
    const [messages, setMessages] = useState([
        {
            type: 'ai',
            content: "👋 Hi! I'm your AI travel concierge. Tell me about your dream trip!",
            timestamp: new Date()
        },
        {
            type: 'ai',
            content: "For example: \"3-day weekend trip to Goa, under ₹15,000, I prefer beaches and good veg food.\"",
            timestamp: new Date()
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = {
            type: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        // Add typing indicator
        const typingMessage = {
            type: 'ai',
            content: '...',
            isTyping: true,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, typingMessage]);

        try {
            const response = await axios.post('/api/plan/create', {
                query: input,
                userId: 'demo-user-123'
            });

            // Remove typing indicator
            setMessages(prev => prev.filter(m => !m.isTyping));

            const aiMessage = {
                type: 'ai',
                content: response.data.message,
                planData: response.data,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, aiMessage]);

            // Notify parent component
            if (onPlanCreated) {
                onPlanCreated(response.data);
            }

        } catch (error) {
            setMessages(prev => prev.filter(m => !m.isTyping));

            const errorMessage = {
                type: 'ai',
                content: `❌ Oops! ${error.response?.data?.error || 'Something went wrong. Please try again.'}`,
                isError: true,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const formatTime = (date) => {
        return new Date(date).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const handleDetailedSubmit = async (formData) => {
        setIsLoading(true);
        setInputMode('simple'); // Switch to chat immediately to show progress

        // Construct a natural language query from form data
        const query = `Trip to ${formData.destination} for ${formData.duration} days`;

        // Add user message
        const userMessage = {
            type: 'user',
            content: `Planning a ${formData.duration}-day trip to ${formData.destination} (Detailed Preferences)`,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMessage]);

        // Add typing indicator
        const typingMessage = {
            type: 'ai',
            content: '...',
            isTyping: true,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, typingMessage]);

        try {
            const response = await axios.post('/api/plan/create', {
                query: query,
                userId: 'demo-user-123',
                preferences: formData,
                origin: formData.origin, // Explicitly pass origin
                is_round_trip: formData.isRoundTrip // Explicitly pass round trip status
            });

            // Remove typing indicator
            setMessages(prev => prev.filter(m => !m.isTyping));

            const aiMessage = {
                type: 'ai',
                content: response.data.message,
                planData: response.data,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, aiMessage]);

            // Notify parent component
            if (onPlanCreated) {
                onPlanCreated(response.data);
            }

        } catch (error) {
            setMessages(prev => prev.filter(m => !m.isTyping));

            const errorMessage = {
                type: 'ai',
                content: `❌ Oops! ${error.response?.data?.error || 'Something went wrong. Please try again.'}`,
                isError: true,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-interface">
            {/* Mode Toggle */}
            <div className="input-mode-toggle">
                <button
                    className={`mode-btn ${inputMode === 'simple' ? 'active' : ''}`}
                    onClick={() => setInputMode('simple')}
                >
                    💬 Quick Chat
                </button>
                <button
                    className={`mode-btn ${inputMode === 'detailed' ? 'active' : ''}`}
                    onClick={() => setInputMode('detailed')}
                >
                    📋 Detailed Form
                </button>
            </div>

            {inputMode === 'detailed' ? (
                <div className="form-scroll-container">
                    <TripPreferencesForm
                        onSubmit={handleDetailedSubmit}
                        isLoading={isLoading}
                        onClose={() => setInputMode('simple')}
                    />
                </div>
            ) : (
                <>
                    <div className="chat-messages">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`message ${message.type} ${message.isTyping ? 'typing' : ''} ${message.isError ? 'error' : ''}`}
                            >
                                <div className="message-icon">
                                    {message.type === 'ai' ? '🤖' : '👤'}
                                </div>
                                <div className="message-content">
                                    {message.isTyping ? (
                                        <div className="typing-indicator">
                                            <span></span>
                                            <span></span>
                                            <span></span>
                                        </div>
                                    ) : (
                                        <>
                                            <p>{message.content}</p>
                                            {message.planData && (
                                                <div className="plan-summary">
                                                    <h4>✨ Trip Summary</h4>
                                                    <div className="summary-grid">
                                                        <div className="summary-item">
                                                            <span className="label">Destination:</span>
                                                            <span className="value">{message.planData.destination}</span>
                                                        </div>
                                                        <div className="summary-item">
                                                            <span className="label">Duration:</span>
                                                            <span className="value">{message.planData.duration.days} days</span>
                                                        </div>
                                                        <div className="summary-item">
                                                            <span className="label">Budget:</span>
                                                            <span className="value">₹{message.planData.budget.toLocaleString()}</span>
                                                        </div>
                                                        <div className="summary-item">
                                                            <span className="label">Estimated:</span>
                                                            <span className="value">₹{message.planData.budgetValidation.estimated.toLocaleString()}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            )}
                                        </>
                                    )}
                                    <span className="message-time">{formatTime(message.timestamp)}</span>
                                </div>
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>

                    <form className="chat-input-area" onSubmit={handleSubmit}>
                        <input
                            type="text"
                            className="input chat-input"
                            placeholder="Describe your ideal trip..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            className="btn btn-primary send-btn"
                            disabled={isLoading || !input.trim()}
                        >
                            {isLoading ? (
                                <span className="spinner small"></span>
                            ) : (
                                '✈️ Plan Trip'
                            )}
                        </button>
                    </form>
                </>
            )}
        </div>
    );
};

export default ChatInterface;
