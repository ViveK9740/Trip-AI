import React from 'react';
import './ItineraryDisplay.css';
import ReviewDisplay from './ReviewDisplay';
import BookingButton from './BookingButton';
import SaveTripButton from './SaveTripButton';

const ItineraryDisplay = ({ itinerary, budgetValidation, destination, tripDetails }) => {
    if (!itinerary || itinerary.length === 0) {
        return null;
    }

    const getActivityIcon = (type) => {
        const icons = {
            sightseeing: '🏛️',
            food: '🍽️',
            activity: '🎯',
            travel: '🚗',
            rest: '😊',
            hotel: '🏨',
            accommodation: '🛏️'
        };
        return icons[type] || '📍';
    };

    const getActivityColor = (type) => {
        const colors = {
            sightseeing: 'hsl(250, 95%, 65%)',
            food: 'hsl(40, 95%, 60%)',
            activity: 'hsl(320, 85%, 60%)',
            travel: 'hsl(180, 90%, 50%)',
            rest: 'hsl(140, 70%, 55%)',
            hotel: 'hsl(280, 90%, 60%)',
            accommodation: 'hsl(280, 90%, 60%)'
        };
        return colors[type] || 'hsl(240, 5%, 55%)';
    };

    return (
        <div className="itinerary-display">
            <div className="itinerary-header">
                <div>
                    <h2 className="gradient-text">📅 Your Perfect Itinerary for {destination}</h2>
                    <p className="text-secondary">
                        {itinerary.length}-day adventure planned just for you
                    </p>
                </div>
                <SaveTripButton 
                    itinerary={itinerary} 
                    tripDetails={{
                        destination: destination,
                        days: itinerary.length,
                        budget: budgetValidation?.budget,
                        ...tripDetails
                    }} 
                />
            </div>

            {/* Budget Overview */}
            {budgetValidation && (
                <div className="budget-overview card-glass">
                    <div className="budget-header">
                        <h3>💰 Budget Analysis</h3>
                        <div className={`budget-status ${budgetValidation.withinBudget ? 'within' : 'over'}`}>
                            {budgetValidation.withinBudget ? '✅ Within Budget' : '⚠️ Over Budget'}
                        </div>
                    </div>

                    {/* Budget Summary */}
                    <div className="budget-summary">
                        <div className="budget-main">
                            <div className="budget-amount">
                                <span className="label">Your Budget</span>
                                <span className="value">₹{budgetValidation.budget.toLocaleString()}</span>
                            </div>
                            <div className="budget-amount">
                                <span className="label">Estimated Cost</span>
                                <span className="value estimated">₹{budgetValidation.estimated.toLocaleString()}</span>
                            </div>
                            <div className="budget-amount">
                                <span className="label">{budgetValidation.withinBudget ? 'Remaining' : 'Over By'}</span>
                                <span className={`value ${budgetValidation.withinBudget ? 'positive' : 'negative'}`}>
                                    ₹{(budgetValidation.withinBudget ? budgetValidation.remaining : budgetValidation.overspent).toLocaleString()}
                                </span>
                            </div>
                        </div>

                        {/* Budget Utilization Bar */}
                        <div className="budget-progress">
                            <div className="progress-header">
                                <span>Budget Utilization</span>
                                <span className="percentage">{budgetValidation.budgetUtilization}%</span>
                            </div>
                            <div className="progress-bar">
                                <div 
                                    className={`progress-fill ${budgetValidation.withinBudget ? 'normal' : 'over'}`}
                                    style={{ width: `${Math.min(budgetValidation.budgetUtilization, 100)}%` }}
                                ></div>
                            </div>
                        </div>
                    </div>

                    {/* Detailed Breakdown */}
                    <div className="budget-breakdown">
                        <h4>💳 Expense Breakdown</h4>
                        <div className="breakdown-items">
                            {[
                                { key: 'accommodation', icon: '🏨', label: 'Accommodation' },
                                { key: 'food', icon: '🍽️', label: 'Food & Dining' },
                                { key: 'attractions', icon: '🎯', label: 'Attractions' },
                                { key: 'activities', icon: '🎪', label: 'Activities' },
                                { key: 'transportation', icon: '🚗', label: 'Transportation' },
                                { key: 'miscellaneous', icon: '🛍️', label: 'Miscellaneous' }
                            ].map(item => {
                                const amount = budgetValidation.breakdown[item.key] || 0;
                                const percentage = ((amount / budgetValidation.estimated) * 100).toFixed(1);
                                return (
                                    <div key={item.key} className="breakdown-item">
                                        <div className="item-header">
                                            <span className="item-icon">{item.icon}</span>
                                            <span className="item-label">{item.label}</span>
                                            <span className="item-amount">₹{amount.toLocaleString()}</span>
                                        </div>
                                        <div className="item-progress">
                                            <div 
                                                className="item-progress-fill"
                                                style={{ 
                                                    width: `${percentage}%`,
                                                    background: `hsl(${220 - percentage * 1.2}, 70%, 60%)`
                                                }}
                                            ></div>
                                        </div>
                                        <div className="item-details">
                                            <span className="item-percentage">{percentage}%</span>
                                            {budgetValidation.perPerson && (
                                                <span className="item-per-person">₹{budgetValidation.perPerson[item.key]?.toLocaleString() || 0}/person</span>
                                            )}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Over Budget Adjustments */}
                    {!budgetValidation.withinBudget && budgetValidation.adjustments && budgetValidation.adjustments.length > 0 && (
                        <div className="budget-adjustments">
                            <h4>💡 Cost-Saving Suggestions</h4>
                            <div className="adjustments-list">
                                {budgetValidation.adjustments.filter(adj => adj.category !== 'summary').map((adj, index) => (
                                    <div key={index} className={`adjustment-item impact-${adj.impact}`}>
                                        <div className="adjustment-content">
                                            <span className="adjustment-category">{adj.category}</span>
                                            <p className="adjustment-suggestion">{adj.suggestion}</p>
                                        </div>
                                        <div className="adjustment-saving">
                                            <span className="saving-label">Save</span>
                                            <span className="saving-amount">₹{adj.potentialSaving.toLocaleString()}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Savings Tips */}
                    {budgetValidation.savingsOpportunities && budgetValidation.savingsOpportunities.length > 0 && (
                        <div className="savings-tips">
                            <h4>✨ Money-Saving Tips</h4>
                            <div className="tips-grid">
                                {budgetValidation.savingsOpportunities.map((tip, index) => (
                                    <div key={index} className="tip-card">
                                        <span className="tip-text">{tip}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Day-wise Timeline */}
            <div className="timeline">
                {itinerary.map((day) => (
                    <div key={day.day} className="day-card card">
                        <div className="day-header">
                            <div className="day-number">Day {day.day}</div>
                            {day.date && (
                                <div className="day-date">
                                    {new Date(day.date).toLocaleDateString('en-US', {
                                        weekday: 'long',
                                        month: 'short',
                                        day: 'numeric'
                                    })}
                                </div>
                            )}
                        </div>

                        <p className="day-summary">{day.summary}</p>

                        <div className="activities-list">
                            {day.activities.map((activity, index) => (
                                <div
                                    key={index}
                                    className="activity-item"
                                    style={{ '--activity-color': getActivityColor(activity.type) }}
                                >
                                    <div className="activity-time">
                                        <span className="time-badge">{activity.time}</span>
                                        <span className="duration">{activity.duration}</span>
                                    </div>

                                    <div className="activity-content">
                                        <div className="activity-header">
                                            <span className="activity-icon">{getActivityIcon(activity.type)}</span>
                                            <h4>{activity.name}</h4>
                                            <span className="activity-type badge">{activity.type}</span>
                                        </div>

                                        {activity.description && (
                                            <p className="activity-description">{activity.description}</p>
                                        )}

                                        {activity.location && activity.location.name && (
                                            <div className="activity-location">
                                                📍 {activity.location.name}
                                                {activity.location.address && `, ${activity.location.address}`}
                                            </div>
                                        )}

                                        {/* Reviews Display */}
                                        {activity.rating && (
                                            <ReviewDisplay
                                                rating={activity.rating}
                                                totalReviews={activity.user_ratings_total}
                                                ratingCategory={activity.rating_category}
                                            />
                                        )}

                                        {/* Booking Button */}
                                        {activity.booking && (
                                            <BookingButton booking={activity.booking} />
                                        )}

                                        <div className="activity-footer">
                                            <span className="cost">₹{activity.estimatedCost}</span>
                                            {activity.tips && (
                                                <span className="tips" title={activity.tips}>💡 Tip available</span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="day-total">
                            Day Total: <span>₹{day.totalCost.toLocaleString()}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ItineraryDisplay;
