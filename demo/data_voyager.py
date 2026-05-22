from datetime import datetime, timezone

def get_voyager_status():
    return {
        "voyager1": {"distance_au": 164.5, "distance_km": 24.6e9, "launch": "1977-09-05"},
        "voyager2": {"distance_au": 137.2, "distance_km": 20.5e9, "launch": "1977-08-20"},
        "updated": datetime.now(timezone.utc).isoformat()
    }
