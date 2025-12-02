
from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path
app = Flask(__name__)
# path to the sqlite database file
APP_DIR = Path(__file__).resolve().parent          # .../database-project/app
PROJECT_ROOT = APP_DIR.parent                      # .../database-project
DB_PATH = PROJECT_ROOT / "sql" / "database.db"     # .../database-project/sql/database.db

def get_db_connection():
    """simple helper to open a sqlite connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # so we can access columns by name
    return conn

# homepage: basic stats for the dashboard
# homepage: basic stats for the dashboard (now from database)
@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # total number of invasive species
    cur.execute("SELECT COUNT(*) FROM invasive_species;")
    total_species = cur.fetchone()[0]

    # total number of sightings
    cur.execute("SELECT COUNT(*) FROM sighting;")
    total_sightings = cur.fetchone()[0]

    # projects that are currently active
    cur.execute("SELECT COUNT(*) FROM eradication_project WHERE status = 'active';")
    active_projects = cur.fetchone()[0]

    # counts by risk level
    cur.execute("SELECT COUNT(*) FROM invasive_species WHERE risk_level = 'high';")
    high_risk = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM invasive_species WHERE risk_level = 'medium';")
    medium_risk = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM invasive_species WHERE risk_level = 'low';")
    low_risk = cur.fetchone()[0]

    conn.close()

    stats = {
        "total_species": total_species,
        "total_sightings": total_sightings,
        "active_projects": active_projects,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
    }

    return jsonify(stats)
# simple route to check server
@app.route("/test")
def test():
    return "test route is working"

# list of invasive species and basic details (now from sqlite)
@app.route("/api/invasive-species")
def list_invasive_species():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            invasive_scientific_name,
            common_name,
            kingdom,
            risk_level,
            spread_rate,
            first_record_in_nl
        FROM invasive_species
        ORDER BY common_name
    """)

    rows = cur.fetchall()
    conn.close()

    # convert sqlite rows to plain dicts for json
    species = []
    for row in rows:
        species.append({
            "invasive_scientific_name": row["invasive_scientific_name"],
            "common_name": row["common_name"],
            "kingdom": row["kingdom"],
            "risk_level": row["risk_level"],
            "spread_rate": row["spread_rate"],
            "first_record_in_nl": row["first_record_in_nl"],
        })

    return jsonify(species)

# list recent sightings (now loaded from sqlite)
@app.route("/api/sightings")
def list_sightings():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            sighting_id,
            observed_date,
            count_estimate,
            photo_url,
            invasive_scientific_name,
            region_id
        FROM sighting
        ORDER BY observed_date DESC, sighting_id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    sightings = []
    for row in rows:
        sightings.append({
            "sighting_id": row["sighting_id"],
            "observed_date": row["observed_date"],
            "count_estimate": row["count_estimate"],
            "photo_url": row["photo_url"],
            "invasive_scientific_name": row["invasive_scientific_name"],
            "region_id": row["region_id"],
        })

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

# list eradication projects (now from sqlite)
@app.route("/api/projects")
def list_projects():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            project_id,
            name_of_project,
            objective,
            status,
            start_date,
            end_date,
            lead_organization,
            budget_planned,
            budget_spent,
            notes
        FROM eradication_project
        ORDER BY start_date DESC, project_id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    projects = []
    for row in rows:
        projects.append({
            "project_id": row["project_id"],
            "name_of_project": row["name_of_project"],
            "objective": row["objective"],
            "status": row["status"],
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "lead_organization": row["lead_organization"],
            "budget_planned": row["budget_planned"],
            "budget_spent": row["budget_spent"],
            "notes": row["notes"],
        })

    return jsonify(projects)


# Q1: high risk species with no control method (real data)
@app.route("/api/queries/1")
def query_1():
    conn = get_db_connection()
    cur = conn.cursor()

    # pick high risk species that are not in species_control_method
    cur.execute("""
        SELECT
            invasive_scientific_name,
            common_name
        FROM invasive_species
        WHERE risk_level = 'high'
          AND invasive_scientific_name NOT IN (
              SELECT invasive_scientific_name
              FROM species_control_method
          );
    """)

    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "invasive_scientific_name": row["invasive_scientific_name"],
            "common_name": row["common_name"],
        })

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

# Q6: population trend (sightings count by year) for one invasive species
@app.route("/api/queries/6")
def query_6():
    # get species from query string, use default if not given
    species_name = request.args.get("species", "Carcinus maenas")

    # later this will use group by year on the sightings table
    trend = [
        {"year": "2022", "total_sightings": 30},
        {"year": "2023", "total_sightings": 45},
        {"year": "2024", "total_sightings": 60},
    ]

    return jsonify({
        "invasive_scientific_name": species_name,
        "trend": trend,
    })
if __name__ == "__main__":
    app.run(debug=True)