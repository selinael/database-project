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

if __name__ == "__main__":
    app.run(debug=True)