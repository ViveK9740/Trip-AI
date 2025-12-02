from typing import Dict, Any
import time
from agents.nlp_agent import nlp_agent
from agents.itinerary_agent import itinerary_agent
from agents.budget_agent import budget_agent


class Orchestrator:
    """
    Agent Orchestrator
    Coordinates all AI agents to create complete travel plans
    """
    
    async def create_travel_plan(
        self, 
        user_query: str, 
        user_id: str,
        user_preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create complete travel plan using all agents"""
        start_time = time.time()
        print("\n🚀 Starting Agent Orchestration...")
        print(f'Query: "{user_query}"')
        
        try:
            # Step 1: Get user preferences (merge with provided)
            preferences = user_preferences or {}
            
            # Step 2: NLP Agent - Parse user query
            print("\n--- Step 1: NLP Processing ---")
            trip_details = await nlp_agent.process(user_query, preferences)
            
            if not trip_details.get("destination"):
                raise Exception("Could not determine destination from query")
            
            # Step 3: Itinerary Agent - Create day-wise plan
            print("\n--- Step 2: Itinerary Generation ---")
            itinerary = await itinerary_agent.process(trip_details)
            
            # Step 4: Budget Agent - Validate and adjust
            print("\n--- Step 3: Budget Validation ---")
            budget_validation = await budget_agent.process(
                itinerary,
                trip_details["budget"],
                trip_details
            )
            
            # Step 5: Create response
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            trip_id = f"temp-{int(time.time() * 1000)}"
            
            response = {
                "success": True,
                "tripId": trip_id,
                "destination": trip_details["destination"],
                "duration": trip_details["duration"],
                "budget": trip_details["budget"],
                "itinerary": itinerary,
                "budgetValidation": budget_validation,
                "processingTime": processing_time,
                "message": (
                    "✅ Your perfect trip is ready!" 
                    if budget_validation["withinBudget"]
                    else "⚠️ Trip plan created but slightly over budget. See suggestions for adjustments."
                )
            }
            
            print(f"\n✅ Orchestration Complete ({processing_time:.0f}ms)")
            return response
            
        except Exception as e:
            print(f"\n❌ Orchestration Error: {str(e)}")
            raise Exception(f"Failed to create travel plan: {str(e)}")


# Singleton instance
orchestrator = Orchestrator()
