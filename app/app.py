
from flask import Flask, jsonify, request
app = Flask(__name__)

# homepage: basic stats for the dashboard
@app.route("/")
def index():
    stats = {
        "total_species": 5,
        "total_sightings": 120,
        "active_projects": 3,
        "high_risk": 2,
        "medium_risk": 2,
        "low_risk": 1,
    }
    return jsonify(stats)

# simple route to check server
@app.route("/test")
def test():
    return "test route is working"

# list of invasive species and basic details
@app.route("/api/invasive-species")
def list_invasive_species():
    # for now this is hard coded data, later we can load it from the database
    species = [
        {
            "invasive_scientific_name": "Carcinus maenas",
            "common_name": "European green crab",
            "kingdom": "Animalia",
            "risk_level": "high",
            "spread_rate": 15.5,
            "first_record_in_nl": "2007-06-15",
        },
        {
            "invasive_scientific_name": "Codium fragile",
            "common_name": "Oyster thief",
            "kingdom": "Plantae",
            "risk_level": "medium",
            "spread_rate": 8.3,
            "first_record_in_nl": "1989-07-10",
        },
        {
            "invasive_scientific_name": "Littorina littorea",
            "common_name": "Common periwinkle",
            "kingdom": "Animalia",
            "risk_level": "low",
            "spread_rate": 2.0,
            "first_record_in_nl": "1860-01-01",
        },
    ]
    return jsonify(species)
# list recent sightings
@app.route("/api/sightings")
def list_sightings():
    # hard coded data for now, will come from the database later
    sightings = [
        {
            "sighting_id": 1,
            "observed_date": "2024-09-10",
            "count_estimate": 20,
            "photo_url": None,
            "invasive_scientific_name": "Carcinus maenas",
            "region_id": 1,
            "reporter_id": 1,
        },
        {
            "sighting_id": 2,
            "observed_date": "2024-09-12",
            "count_estimate": 10,
            "photo_url": None,
            "invasive_scientific_name": "Codium fragile",
            "region_id": 2,
            "reporter_id": 2,
        },
    ]
    return jsonify(sightings)

# create a new sighting (dummy implementation for now)
@app.route("/api/sightings", methods=["POST"])
def create_sighting():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "request body must be json"}), 400

    # simple required fields based on the schema
    required_fields = ["invasive_scientific_name", "region_id", "reporter_id", "count_estimate"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400

    # in the final version this will insert into the database
    # for now we just pretend it worked and return the data back
    new_sighting = {
        "sighting_id": 999,  # placeholder id
        "observed_date": data.get("observed_date", "2024-11-30"),
        "count_estimate": data["count_estimate"],
        "photo_url": data.get("photo_url"),
        "invasive_scientific_name": data["invasive_scientific_name"],
        "region_id": data["region_id"],
        "reporter_id": data["reporter_id"],
    }

    return jsonify({"message": "sighting created (placeholder, no db yet)", "sighting": new_sighting}), 201
# list eradication projects
@app.route("/api/projects")
def list_projects():
    # dummy data for now, later will come from the database
    projects = [
        {
            "project_id": 1,
            "name_of_project": "Operation Shoreline",
            "objective": "Reduce green crab numbers along the Avalon coast.",
            "status": "active",
            "start_date": "2023-05-01",
            "end_date": None,
            "lead_organization": "DFO Newfoundland",
            "budget_planned": 25000.0,
            "budget_spent": 8000.0,
            "notes": "focus on trap-based removal",
        },
        {
            "project_id": 2,
            "name_of_project": "Harbour Cleanup",
            "objective": "Control tunicate spread in major harbours.",
            "status": "completed",
            "start_date": "2022-04-15",
            "end_date": "2022-10-30",
            "lead_organization": "City of St. John's",
            "budget_planned": 18000.0,
            "budget_spent": 17500.0,
            "notes": "ran as a pilot project",
        },
    ]
    return jsonify(projects)


# Q1: high risk species with no control method
@app.route("/api/queries/1")
def query_1():
    # this will come from joins later, for now just hard coded
    result = [
        {
            "invasive_scientific_name": "Carcinus maenas",
            "common_name": "European green crab",
        }
    ]
    return jsonify(result)
# Q2: sightings count by region and risk level
@app.route("/api/queries/2")
def query_2():
    # later this will use group by on the sightings table
    data = [
        {"region": "Avalon Peninsula", "risk_level": "high", "count": 40},
        {"region": "Avalon Peninsula", "risk_level": "medium", "count": 10},
        {"region": "Gros Morne", "risk_level": "medium", "count": 15},
        {"region": "Terra Nova", "risk_level": "low", "count": 5},
    ]
    return jsonify(data)

# Q3: projects that use 'Manual Removal' as a control method
@app.route("/api/queries/3")
def query_3():
    # later this will join eradication_project and method_project tables
    data = [
        {
            "project_id": 1,
            "name_of_project": "Operation Shoreline",
            "status": "active",
            "method_name": "Manual Removal",
        },
        {
            "project_id": 3,
            "name_of_project": "Harbour Pilot Study",
            "status": "completed",
            "method_name": "Manual Removal",
        },
    ]
    return jsonify(data)

# Q4: regions with sightings but no active projects
@app.route("/api/queries/4")
def query_4():
    # later this will compare regions in sightings vs regions in active projects
    data = [
        {"region_id": 2, "region_name": "Burin Peninsula"},
        {"region_id": 5, "region_name": "Bonavista"},
    ]
    return jsonify(data)

# Q5: native species impacted by high risk invasives
@app.route("/api/queries/5")
def query_5():
    # later this will join native_species, impact and invasive_species
    data = [
        {
            "native_scientific_name": "Salmo salar",
            "native_common_name": "Atlantic salmon",
            "threat_count": 2,
        },
        {
            "native_scientific_name": "Gadus morhua",
            "native_common_name": "Atlantic cod",
            "threat_count": 1,
        },
    ]
    return jsonify(data)
if __name__ == "__main__":
    app.run(debug=True)