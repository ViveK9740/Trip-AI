import React from 'react';
import './ReviewDisplay.css';

const ReviewDisplay = ({ rating, totalReviews, ratingCategory }) => {
    if (!rating || rating === 0) {
        return null;
    }

    // Generate star display
    const renderStars = () => {
        const stars = [];
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;

        for (let i = 0; i < 5; i++) {
            if (i < fullStars) {
                stars.push(<span key={i} className="star filled">★</span>);
            } else if (i === fullStars && hasHalfStar) {
                stars.push(<span key={i} className="star half">★</span>);
            } else {
                stars.push(<span key={i} className="star empty">☆</span>);
            }
        }
        return stars;
    };

    // Get color based on rating
    const getRatingColor = () => {
        if (rating >= 4.5) return 'hsl(140, 70%, 55%)'; // Green
        if (rating >= 4.0) return 'hsl(100, 65%, 50%)'; // Light green
        if (rating >= 3.5) return 'hsl(50, 90%, 55%)';  // Yellow
        if (rating >= 3.0) return 'hsl(30, 85%, 55%)';  // Orange
        return 'hsl(0, 70%, 55%)'; // Red
    };

    return (
        <div className="review-display">
            <div className="stars-container">
                {renderStars()}
            </div>
            <div className="rating-info">
                <span
                    className="rating-score"
                    style={{ color: getRatingColor() }}
                >
                    {rating.toFixed(1)}
                </span>
                {ratingCategory && (
                    <span className="rating-category">{ratingCategory}</span>
                )}
            </div>
            {totalReviews > 0 && (
                <span className="review-count">
                    ({totalReviews.toLocaleString()} reviews)
                </span>
            )}
        </div>
    );
};

export default ReviewDisplay;
