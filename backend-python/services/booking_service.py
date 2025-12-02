from typing import Dict, Optional
from urllib.parse import quote_plus


class BookingService:
    """
    Service for generating booking links to partner platforms
    Uses affiliate links for monetization opportunities
    """
    
    def generate_hotel_link(
        self, 
        city: str, 
        checkin: Optional[str] = None, 
        checkout: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate hotel booking links"""
        city_encoded = quote_plus(city)
        
        links = {
            "makemytrip": f"https://www.makemytrip.com/hotels/hotel-listing/?city={city_encoded}",
            "booking": f"https://www.booking.com/searchresults.html?ss={city_encoded}",
            "primary": f"https://www.makemytrip.com/hotels/hotel-listing/?city={city_encoded}"
        }
        
        # Add dates if provided
        if checkin and checkout:
            links["makemytrip"] += f"&checkin={checkin}&checkout={checkout}"
            links["booking"] += f"&checkin={checkin}&checkout={checkout}"
        
        return links
    
    def generate_restaurant_link(
        self, 
        restaurant_name: str, 
        city: str
    ) -> Dict[str, str]:
        """Generate restaurant booking/discovery links"""
        restaurant_encoded = quote_plus(restaurant_name)
        city_encoded = quote_plus(city)
        
        links = {
            "zomato": f"https://www.zomato.com/{city_encoded}/restaurants?q={restaurant_encoded}",
            "swiggy": f"https://www.swiggy.com/restaurants/{city_encoded}",
            "primary": f"https://www.zomato.com/{city_encoded}/restaurants?q={restaurant_encoded}"
        }
        
        return links
    
    def generate_activity_link(
        self, 
        activity_name: str, 
        city: str
    ) -> Dict[str, str]:
        """Generate activity booking links"""
        activity_encoded = quote_plus(f"{activity_name} {city}")
        city_encoded = quote_plus(city)
        
        links = {
            "getyourguide": f"https://www.getyourguide.com/s/?q={activity_encoded}",
            "thrillophilia": f"https://www.thrillophilia.com/search?q={activity_encoded}",
            "tripadvisor": f"https://www.tripadvisor.in/Search?q={activity_encoded}",
            "primary": f"https://www.getyourguide.com/s/?q={activity_encoded}"
        }
        
        return links
    
    def generate_booking_for_activity(
        self, 
        activity: Dict, 
        destination: str
    ) -> Optional[Dict[str, str]]:
        """Generate appropriate booking link based on activity type"""
        activity_type = activity.get("type", "").lower()
        activity_name = activity.get("name", "")
        
        if not activity_name:
            return None
        
        # Determine booking type
        if activity_type in ["restaurant", "food", "dinner", "lunch", "breakfast"]:
            return {
                **self.generate_restaurant_link(activity_name, destination),
                "type": "restaurant",
                "label": "Reserve Table"
            }
        elif activity_type in ["hotel", "accommodation"]:
            return {
                **self.generate_hotel_link(destination),
                "type": "hotel",
                "label": "Book Hotel"
            }
        elif activity_type in ["activity", "sightseeing", "adventure"]:
            return {
                **self.generate_activity_link(activity_name, destination),
                "type": "activity",
                "label": "Book Activity"
            }
        else:
            # Default to activity link
            return {
                **self.generate_activity_link(activity_name, destination),
                "type": "general",
                "label": "Explore Options"
            }


# Singleton instance
booking_service = BookingService()
