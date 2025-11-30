from flask import Flask, jsonify

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
if __name__ == "__main__":
    app.run(debug=True)