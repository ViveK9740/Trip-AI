from typing import Dict, Any, List


class BudgetAgent:
    """
    Budget Agent
    Validates itineraries against budget constraints and provides recommendations
    """
    
    # Accommodation pricing per night (base rates - realistic Indian prices)
    ACCOMMODATION_RATES = {
        "budget": {"min": 600, "max": 1200},      # Budget hotels, hostels
        "mid_range": {"min": 1500, "max": 3500}, # 3-4 star hotels
        "luxury": {"min": 5000, "max": 12000}    # 5-star hotels, resorts
    }
    
    # Meal costs per person (realistic Indian dining costs)
    MEAL_COSTS = {
        "budget": {"breakfast": 80, "lunch": 150, "dinner": 200},      # Street food, local eateries
        "mid_range": {"breakfast": 150, "lunch": 300, "dinner": 400}, # Standard restaurants
        "luxury": {"breakfast": 300, "lunch": 600, "dinner": 800}     # Fine dining
    }
    
    # Transportation base costs (₹ per km or fixed rates)
    TRANSPORT_COSTS = {
        "public_transport": {"per_km": 1.5, "city_daily": 150},  # Bus/metro
        "own_vehicle": {"fuel_per_km": 6, "toll_daily": 100},    # Petrol car
        "rental": {"per_day": 2000, "fuel_per_km": 6},           # Rental car with fuel
        "flexible": {"per_km": 12, "city_daily": 300}            # Mix of auto/taxi/bus
    }
    
    # Activity/Attraction entry fees (average per person)
    ACTIVITY_COSTS = {
        "monument": 50,      # Historical monuments (ASI sites)
        "fort": 100,         # Forts and palaces
        "museum": 50,        # Museums
        "temple": 0,         # Temples (usually free)
        "beach": 0,          # Beaches (free)
        "waterfall": 20,     # Waterfalls (nominal entry)
        "viewpoint": 0,      # Viewpoints (usually free)
        "park": 30,          # Parks and gardens
        "adventure": 800,    # Adventure activities (parasailing, rafting, etc.)
        "water_sports": 500, # Water sports
        "amusement_park": 600, # Theme/amusement parks
        "zoo": 80,           # Zoos and aquariums
        "wildlife": 1500,    # Wildlife sanctuary (with safari)
        "boat_ride": 200,    # Boat rides
        "shopping": 500      # Shopping budget per visit
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
        adults = trip_details.get("travelers", {}).get("adults", 1)
        children = trip_details.get("travelers", {}).get("children", 0)
        travelers = adults + children
        
        # Get preferences
        preferences = trip_details.get("preferences", {})
        accommodation_type = preferences.get("accommodation_type", "mid_range")
        transport_mode = preferences.get("transport_mode", "flexible")
        origin = trip_details.get("origin")
        destination = trip_details.get("destination", "")
        
        # 1. ACCOMMODATION COSTS
        if nights > 0:
            rate_range = self.ACCOMMODATION_RATES.get(accommodation_type, self.ACCOMMODATION_RATES["mid_range"])
            avg_rate = (rate_range["min"] + rate_range["max"]) / 2
            # Rooms: 1 room for 1-2 people, 2 rooms for 3-4 people, etc.
            rooms_needed = max(1, (travelers + 1) // 2)
            accommodation_per_night = avg_rate * rooms_needed
            accommodation = round(accommodation_per_night * nights)
        else:
            accommodation = 0
        
        # 2. FOOD COSTS (count actual meals from itinerary)
        meal_rates = self.MEAL_COSTS.get(accommodation_type, self.MEAL_COSTS["mid_range"])
        
        # Count meals from itinerary
        breakfast_count = lunch_count = dinner_count = 0
        for day in itinerary:
            for activity in day.get("activities", []):
                if activity.get("type") == "food":
                    desc = activity.get("description", "").lower()
                    if "breakfast" in desc:
                        breakfast_count += 1
                    elif "lunch" in desc:
                        lunch_count += 1
                    elif "dinner" in desc:
                        dinner_count += 1
        
        # Calculate food cost based on actual meals
        food = round((
            breakfast_count * meal_rates["breakfast"] +
            lunch_count * meal_rates["lunch"] +
            dinner_count * meal_rates["dinner"]
        ) * travelers)
        
        # If no meals counted, use default (3 per day)
        if breakfast_count + lunch_count + dinner_count == 0:
            daily_food = sum(meal_rates.values()) * travelers
            food = round(daily_food * days)
        
        # 3. ATTRACTIONS & ACTIVITIES COSTS (estimate based on activity types)
        attractions_cost = 0
        activities_cost = 0
        
        for day in itinerary:
            for activity in day.get("activities", []):
                act_type = activity.get("type", "")
                name = activity.get("name", "").lower()
                
                if act_type == "sightseeing":
                    # Estimate based on place type
                    cost_per_person = 0
                    if any(word in name for word in ["fort", "palace"]):
                        cost_per_person = self.ACTIVITY_COSTS["fort"]
                    elif any(word in name for word in ["monument", "memorial"]):
                        cost_per_person = self.ACTIVITY_COSTS["monument"]
                    elif "museum" in name or "gallery" in name:
                        cost_per_person = self.ACTIVITY_COSTS["museum"]
                    elif any(word in name for word in ["temple", "church", "mosque"]):
                        cost_per_person = self.ACTIVITY_COSTS["temple"]
                    elif any(word in name for word in ["beach", "coast"]):
                        cost_per_person = self.ACTIVITY_COSTS["beach"]
                    elif "waterfall" in name or "falls" in name:
                        cost_per_person = self.ACTIVITY_COSTS["waterfall"]
                    elif "viewpoint" in name or "view point" in name:
                        cost_per_person = self.ACTIVITY_COSTS["viewpoint"]
                    elif any(word in name for word in ["park", "garden"]):
                        cost_per_person = self.ACTIVITY_COSTS["park"]
                    elif any(word in name for word in ["zoo", "aquarium"]):
                        cost_per_person = self.ACTIVITY_COSTS["zoo"]
                    elif "wildlife" in name or "sanctuary" in name or "safari" in name:
                        cost_per_person = self.ACTIVITY_COSTS["wildlife"]
                    else:
                        cost_per_person = 50  # Default sightseeing
                    
                    attractions_cost += cost_per_person * travelers
                
                elif act_type == "activity":
                    # Adventure/special activities
                    cost_per_person = 0
                    if any(word in name for word in ["water sport", "jet ski", "parasailing", "banana boat"]):
                        cost_per_person = self.ACTIVITY_COSTS["water_sports"]
                    elif any(word in name for word in ["adventure", "rafting", "trekking", "paragliding"]):
                        cost_per_person = self.ACTIVITY_COSTS["adventure"]
                    elif "amusement" in name or "theme park" in name:
                        cost_per_person = self.ACTIVITY_COSTS["amusement_park"]
                    elif "boat" in name or "cruise" in name:
                        cost_per_person = self.ACTIVITY_COSTS["boat_ride"]
                    elif "shop" in name or "market" in name:
                        cost_per_person = self.ACTIVITY_COSTS["shopping"]
                    else:
                        cost_per_person = 300  # Default activity
                    
                    activities_cost += cost_per_person * travelers
        
        attractions_cost = round(attractions_cost)
        activities_cost = round(activities_cost)
        
        # 4. TRANSPORTATION COSTS (realistic calculation)
        transportation = self._calculate_transport_cost(
            origin, destination, days, travelers, transport_mode
        )
        
        # 5. MISCELLANEOUS (tips, shopping, emergencies)
        # 5-10% of (accommodation + food + activities)
        base_cost = accommodation + food + attractions_cost + activities_cost
        miscellaneous = round(base_cost * 0.08)
        
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
    
    def _calculate_transport_cost(
        self,
        origin: str,
        destination: str,
        days: int,
        travelers: int,
        transport_mode: str
    ) -> float:
        """Calculate realistic transportation costs"""
        
        # Estimate distance between cities (km)
        distance = self._estimate_distance(origin, destination)
        
        transport_info = self.TRANSPORT_COSTS.get(transport_mode, self.TRANSPORT_COSTS["flexible"])
        
        if transport_mode == "public_transport":
            # Intercity travel (bus/train) + daily city transport
            if distance > 0:
                intercity_cost = distance * 0.5 * travelers  # ₹0.5 per km per person (bus/train)
                intercity_cost *= 2  # Round trip
            else:
                intercity_cost = 0
            city_transport = transport_info["city_daily"] * days * travelers
            return round(intercity_cost + city_transport)
        
        elif transport_mode == "own_vehicle":
            # Fuel + tolls
            if distance > 0:
                fuel_cost = distance * transport_info["fuel_per_km"] * 2  # Round trip
                toll_cost = transport_info["toll_daily"] * ((distance // 200) + 1) * 2  # Tolls
            else:
                fuel_cost = 0
                toll_cost = 0
            city_fuel = 30 * transport_info["fuel_per_km"] * days  # 30km daily city driving
            return round(fuel_cost + toll_cost + city_fuel)
        
        elif transport_mode == "rental":
            # Rental fee + fuel
            rental_fee = transport_info["per_day"] * days
            if distance > 0:
                fuel = (distance * 2 + 30 * days) * transport_info["fuel_per_km"]
            else:
                fuel = 30 * days * transport_info["fuel_per_km"]
            return round(rental_fee + fuel)
        
        else:  # flexible (mix of transport)
            # Taxi/auto for city + intercity
            if distance > 0:
                intercity = distance * 8 * 2  # ₹8 per km (shared taxi)
            else:
                intercity = 0
            city_travel = transport_info["city_daily"] * days
            return round(intercity + city_travel)
    
    def _estimate_distance(self, origin: str, destination: str) -> int:
        """Estimate distance between cities (very rough estimates)"""
        if not origin or not destination:
            return 0
        
        # Common city pairs (km)
        city_distances = {
            ("bangalore", "hyderabad"): 570,
            ("bangalore", "goa"): 560,
            ("bangalore", "mysore"): 150,
            ("mumbai", "goa"): 580,
            ("mumbai", "pune"): 150,
            ("delhi", "jaipur"): 280,
            ("delhi", "agra"): 230,
            ("chennai", "pondicherry"): 160,
            ("chennai", "bangalore"): 350,
            ("kolkata", "darjeeling"): 600,
        }
        
        # Normalize city names
        origin_norm = origin.lower().split()[0] if origin else ""
        dest_norm = destination.lower().split()[0] if destination else ""
        
        # Check direct match
        for (city1, city2), dist in city_distances.items():
            if (origin_norm in city1 or city1 in origin_norm) and \
               (dest_norm in city2 or city2 in dest_norm):
                return dist
            if (origin_norm in city2 or city2 in origin_norm) and \
               (dest_norm in city1 or city1 in dest_norm):
                return dist
        
        # If no match, assume moderate distance (local trip)
        if origin_norm and dest_norm and origin_norm != dest_norm:
            return 300  # Default 300km for unknown routes
        
        return 0  # Same city or no origin
    
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
