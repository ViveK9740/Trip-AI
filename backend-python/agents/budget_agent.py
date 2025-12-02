from typing import Dict, Any, List


class BudgetAgent:
    """
    Budget Agent
    Validates itineraries against budget constraints and provides recommendations
    """
    
    # Accommodation pricing per night (base rates)
    ACCOMMODATION_RATES = {
        "budget": {"min": 800, "max": 1500},
        "mid_range": {"min": 2500, "max": 5000},
        "luxury": {"min": 8000, "max": 15000}
    }
    
    # Meal costs per person
    MEAL_COSTS = {
        "budget": {"breakfast": 100, "lunch": 200, "dinner": 250},
        "mid_range": {"breakfast": 200, "lunch": 400, "dinner": 500},
        "luxury": {"breakfast": 400, "lunch": 800, "dinner": 1000}
    }
    
    async def process(
        self, 
        itinerary: List[Dict[str, Any]], 
        budget: float, 
        trip_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process itinerary and validate budget"""
        print("💰 Budget Agent: Validating budget...")
        
        try:
            # Calculate costs
            breakdown = self._calculate_budget_breakdown(itinerary, trip_details)
            total = breakdown["total"]
            within_budget = total <= budget
            remaining = budget - total if within_budget else 0
            overspent = total - budget if not within_budget else 0
            
            adjustments = []
            if not within_budget:
                adjustments = self._generate_adjustments(breakdown, budget, total, trip_details)
            
            result = {
                "withinBudget": within_budget,
                "budget": budget,
                "estimated": total,
                "remaining": remaining,
                "overspent": overspent,
                "breakdown": breakdown,
                "perPerson": self._calculate_per_person_cost(breakdown, trip_details),
                "adjustments": adjustments,
                "savingsOpportunities": self._identify_savings(breakdown, trip_details),
                "budgetUtilization": round((total / budget) * 100, 1) if budget > 0 else 0
            }
            
            status = "✅" if within_budget else "⚠️"
            print(f"{status} Budget Agent: ₹{total:,.0f} / ₹{budget:,.0f} ({result['budgetUtilization']}%)")
            return result
            
        except Exception as e:
            print(f"❌ Budget Agent Error: {str(e)}")
            raise
    
    def _calculate_budget_breakdown(
        self, 
        itinerary: List[Dict[str, Any]], 
        trip_details: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate detailed budget breakdown with realistic pricing"""
        days = trip_details["duration"]["days"]
        nights = days - 1 if days > 1 else 0
        travelers = trip_details.get("travelers", {}).get("adults", 1) + trip_details.get("travelers", {}).get("children", 0)
        accommodation_type = trip_details.get("accommodation_type", "mid_range")
        
        # Accommodation costs (realistic per-night pricing)
        if nights > 0:
            rate_range = self.ACCOMMODATION_RATES.get(accommodation_type, self.ACCOMMODATION_RATES["mid_range"])
            avg_rate = (rate_range["min"] + rate_range["max"]) / 2
            # Single room for 1-2 people, additional rooms for more
            rooms_needed = max(1, (travelers + 1) // 2)
            accommodation_per_night = avg_rate * rooms_needed
            accommodation = round(accommodation_per_night * nights)
        else:
            accommodation = 0
        
        # Food costs (realistic meal pricing per person)
        meal_rates = self.MEAL_COSTS.get(accommodation_type, self.MEAL_COSTS["mid_range"])
        meals_per_day = 3  # breakfast, lunch, dinner
        daily_food_cost = sum(meal_rates.values()) * travelers
        food = round(daily_food_cost * days)
        
        # Activities and attractions (sum from itinerary)
        activities_cost = 0
        attractions_cost = 0
        for day in itinerary:
            for activity in day.get("activities", []):
                cost = activity.get("estimated_cost", 0)
                if activity.get("type") in ["sightseeing", "activity"]:
                    attractions_cost += cost
                elif activity.get("type") != "food":
                    activities_cost += cost
        
        # Transportation (based on distance and mode)
        transport_mode = trip_details.get("transport_mode", "public")
        transport_multipliers = {
            "public": 0.15,  # 15% of budget
            "rental": 0.25,  # 25% of budget
            "own_vehicle": 0.12,  # 12% of budget (fuel only)
            "flight": 0.30  # 30% of budget
        }
        budget = trip_details["budget"]
        transportation = round(budget * transport_multipliers.get(transport_mode, 0.15))
        
        # Miscellaneous (shopping, tips, emergencies)
        miscellaneous = round(budget * 0.08)
        
        total = accommodation + food + activities_cost + attractions_cost + transportation + miscellaneous
        
        return {
            "accommodation": accommodation,
            "food": food,
            "activities": activities_cost,
            "attractions": attractions_cost,
            "transportation": transportation,
            "miscellaneous": miscellaneous,
            "total": round(total),
            "accommodationPerNight": round(accommodation / nights) if nights > 0 else 0,
            "foodPerDay": round(food / days) if days > 0 else 0
        }
    
    def _calculate_per_person_cost(
        self,
        breakdown: Dict[str, float],
        trip_details: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate per-person cost breakdown"""
        travelers = trip_details.get("travelers", {}).get("adults", 1) + trip_details.get("travelers", {}).get("children", 0)
        travelers = max(1, travelers)
        
        return {
            "accommodation": round(breakdown["accommodation"] / travelers),
            "food": round(breakdown["food"] / travelers),
            "activities": round(breakdown["activities"] / travelers),
            "attractions": round(breakdown["attractions"] / travelers),
            "transportation": round(breakdown["transportation"] / travelers),
            "miscellaneous": round(breakdown["miscellaneous"] / travelers),
            "total": round(breakdown["total"] / travelers)
        }
    
    def _generate_adjustments(
        self, 
        breakdown: Dict[str, float], 
        budget: float, 
        total: float,
        trip_details: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate adjustment suggestions when over budget"""
        over_by = total - budget
        adjustments = []
        accommodation_type = trip_details.get("accommodation_type", "mid_range")
        
        # Suggest downgrading accommodation
        if accommodation_type in ["luxury", "mid_range"]:
            target_type = "mid_range" if accommodation_type == "luxury" else "budget"
            current_rate = (self.ACCOMMODATION_RATES[accommodation_type]["min"] + self.ACCOMMODATION_RATES[accommodation_type]["max"]) / 2
            target_rate = (self.ACCOMMODATION_RATES[target_type]["min"] + self.ACCOMMODATION_RATES[target_type]["max"]) / 2
            nights = trip_details["duration"]["days"] - 1
            saving = round((current_rate - target_rate) * nights)
            if saving > 0:
                adjustments.append({
                    "category": "accommodation",
                    "suggestion": f"Downgrade from {accommodation_type.replace('_', ' ')} to {target_type.replace('_', ' ')} accommodation",
                    "potentialSaving": saving,
                    "impact": "moderate"
                })
        
        # Suggest reducing paid activities
        total_activities = breakdown["activities"] + breakdown["attractions"]
        if total_activities > budget * 0.25:
            saving = round(total_activities * 0.30)
            adjustments.append({
                "category": "activities",
                "suggestion": "Prioritize free attractions (beaches, parks, temples) over paid activities",
                "potentialSaving": saving,
                "impact": "low"
            })
        
        # Suggest cheaper transportation
        transport_mode = trip_details.get("transport_mode", "public")
        if transport_mode in ["rental", "flight"]:
            current_pct = 0.25 if transport_mode == "rental" else 0.30
            target_pct = 0.15
            saving = round(budget * (current_pct - target_pct))
            if saving > 0:
                adjustments.append({
                    "category": "transportation",
                    "suggestion": "Switch to public transport (buses, trains) instead of private vehicles",
                    "potentialSaving": saving,
                    "impact": "moderate"
                })
        
        # Suggest reducing trip duration
        if len(adjustments) < 3 and trip_details["duration"]["days"] > 3:
            days_to_reduce = 1
            saving_per_day = breakdown["foodPerDay"] + breakdown["accommodationPerNight"]
            saving = round(saving_per_day * days_to_reduce)
            adjustments.append({
                "category": "duration",
                "suggestion": f"Reduce trip by {days_to_reduce} day(s) to save on accommodation and meals",
                "potentialSaving": saving,
                "impact": "high"
            })
        
        # Add summary
        total_savings = sum(adj.get("potentialSaving", 0) for adj in adjustments)
        adjustments.append({
            "category": "summary",
            "suggestion": f"You're ₹{over_by:,} over budget. These suggestions could save ₹{total_savings:,}",
            "potentialSaving": total_savings,
            "impact": "summary"
        })
        
        return adjustments
    
    def _identify_savings(self, breakdown: Dict[str, float], trip_details: Dict[str, Any]) -> List[str]:
        """Identify savings opportunities even when within budget"""
        tips = []
        total = breakdown["total"]
        destination = trip_details.get("destination", "").lower()
        
        # Food savings
        if breakdown["food"] > total * 0.30:
            tips.append("💡 Try local street food and dhabas for authentic meals at 50-70% lower cost")
        else:
            tips.append("💡 Mix fine dining with local eateries to balance experience and budget")
        
        # Accommodation savings
        if breakdown["accommodation"] > total * 0.35:
            tips.append("🏨 Book 30+ days in advance for up to 25% discount on hotels")
            tips.append("🏨 Consider homestays or guesthouses for authentic local experience")
        
        # Activity savings
        tips.append("🎟️ Look for combo tickets at tourist spots - often 15-20% cheaper")
        tips.append("🎟️ Many temples, beaches, and parks are free - plan these first")
        
        # Transport savings
        transport_mode = trip_details.get("transport_mode", "public")
        if transport_mode != "public":
            tips.append("🚌 Use public transport for city travel - saves 60-70% vs private cabs")
        
        # Timing savings
        tips.append("⏰ Visit attractions during off-peak hours for better rates and fewer crowds")
        
        # Destination-specific tips
        if "goa" in destination:
            tips.append("🏖️ Goa tip: Beaches are free! Focus budget on water sports and nightlife")
        elif "kerala" in destination:
            tips.append("🌴 Kerala tip: Book houseboat packages in advance for better deals")
        elif "jaipur" in destination or "rajasthan" in destination:
            tips.append("🏰 Rajasthan tip: Composite tickets for monuments save 30-40%")
        
        return tips[:6]  # Return top 6 tips


# Singleton instance
budget_agent = BudgetAgent()
