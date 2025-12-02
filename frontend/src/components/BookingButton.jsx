import React from 'react';
import './BookingButton.css';

const BookingButton = ({ booking }) => {
    if (!booking || !booking.primary) {
        return null;
    }

    const handleBookingClick = (url) => {
        // Track click for analytics (future enhancement)
        console.log('Booking clicked:', url);
        window.open(url, '_blank', 'noopener,noreferrer');
    };

    // Get button style based on booking type
    const getButtonStyle = () => {
        const styles = {
            restaurant: {
                icon: '🍽️',
                gradient: 'linear-gradient(135deg, hsl(40, 95%, 60%), hsl(30, 90%, 55%))'
            },
            hotel: {
                icon: '🏨',
                gradient: 'linear-gradient(135deg, hsl(250, 95%, 65%), hsl(280, 90%, 60%))'
            },
            activity: {
                icon: '🎯',
                gradient: 'linear-gradient(135deg, hsl(320, 85%, 60%), hsl(340, 80%, 55%))'
            },
            general: {
                icon: '🔗',
                gradient: 'linear-gradient(135deg, hsl(200, 90%, 55%), hsl(220, 85%, 50%))'
            }
        };

        return styles[booking.type] || styles.general;
    };

    const style = getButtonStyle();

    return (
        <div className="booking-button-container">
            <button
                className="booking-button"
                onClick={() => handleBookingClick(booking.primary)}
                style={{ background: style.gradient }}
            >
                <span className="booking-icon">{style.icon}</span>
                <span className="booking-label">{booking.label || 'Book Now'}</span>
            </button>
        </div>
    );
};

export default BookingButton;
