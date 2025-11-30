from flask import Flask, jsonify

# simple flask app for the backend
app = Flask(__name__)

# homepage: return basic stats as json
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

# extra route just to check server quickly
@app.route("/test")
def test():
    return "test route is working"

if __name__ == "__main__":
    app.run(debug=True)