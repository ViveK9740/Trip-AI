import os
import glob
import json

def analyze_logs():
    log_dir = "d:\\Agentic- Tripai\\backend-python\\logs"
    list_of_files = glob.glob(f"{log_dir}\\*.log")
    
    if not list_of_files:
        print("No log files found")
        return

    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Analyzing latest log: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Search for key statistics
        keywords = [
            "PLACES DATA SENT TO GEMINI",
            "GEMINI ITINERARY RESPONSE",
            "ITINERARY AGENT EXCEPTION"
        ]
        
        print("\n--- Key Log Events ---")
        for line in content.splitlines():
            for kw in keywords:
                if kw in line:
                    print(f"FOUND: {kw}")
                    if "ITINERARY AGENT EXCEPTION" in line:
                        print(f"RAW EXCEPTION LINE: {line[:500]}...") # Print first 500 chars



    print("\n--- End Analysis ---")


analyze_logs()
