def generate_recommendation(priority, event_cause, zone, requires_road_closure):
    r = {
        "priority": priority, "zone": zone, "event_cause": event_cause,
        "alert_level": "Red" if priority == "High" else "Yellow",
        "response_team": [], "recommended_actions": [],
        "officers": 8 if priority == "High" else 3,
        "barricades": 12 if priority == "High" else 4,
        "impact_category": "Zone-Level Impact" if priority == "High" else "Local Impact",
    }
    responses = {
        "accident": (["Traffic Police","Emergency Services","Ambulance Support"],
                     ["Secure accident scene","Clear damaged vehicles","Coordinate emergency response"]),
        "vehicle_breakdown": (["Traffic Police","Tow Truck Unit"],
                              ["Dispatch tow truck","Remove disabled vehicle","Restore traffic flow"]),
        "construction": (["Road Maintenance Team","Traffic Police"],
                         ["Deploy temporary traffic signs","Monitor lane closures","Guide vehicles to alternate routes"]),
        "water_logging": (["Municipal Drainage Team","Traffic Police"],
                          ["Pump out water","Inspect road conditions","Divert traffic"]),
        "public_event": (["Traffic Police","Crowd Management Team"],
                         ["Deploy crowd barriers","Control pedestrian crossings","Manage event traffic flow"]),
        "congestion": (["Traffic Monitoring Unit"],
                       ["Optimize signal timing","Monitor congestion levels","Issue traffic advisory"]),
        "tree_fall": (["Municipal Emergency Team","Traffic Police"],
                      ["Remove fallen tree","Inspect roadway","Redirect traffic"]),
    }
    r["response_team"], r["recommended_actions"] = responses.get(
        event_cause,
        (["Traffic Monitoring Unit"],["Monitor situation","Dispatch field team if required"])
    )
    if requires_road_closure:
        r["barricades"] += 4
        r["recommended_actions"] += ["Activate diversion route","Deploy road barricades",
                                     "Notify navigation services","Issue public traffic advisory"]
    if priority == "High":
        r["recommended_actions"] += ["Dispatch rapid response team",
                                     "Increase signal monitoring","Escalate to traffic control center"]
    return r
