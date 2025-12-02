
from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request , render_template
import sqlite3
from pathlib import Path
from datetime import date
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

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')
# path to the sqlite database file
APP_DIR = Path(__file__).resolve().parent          # .../database-project/app
PROJECT_ROOT = APP_DIR.parent                      # .../database-project
DB_PATH = APP_DIR / "database.db"     # .../database-project/sql/database.db

def get_db_connection():
    """simple helper to open a sqlite connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # so we can access columns by name
    conn.execute("PRAGMA foreign_keys = ON;")  # enforce FK constraints
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

# list recent sightings

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
# create a new sighting (real insert into SQLite)
@app.route("/api/sightings", methods=["POST"])
def create_sighting():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "request body must be json"}), 400

    # required fields based on the sighting table
    required_fields = ["invasive_scientific_name", "region_id", "count_estimate"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400

    # basic type handling / defaults
    invasive_scientific_name = data["invasive_scientific_name"]
    region_id = int(data["region_id"])
    count_estimate = int(data["count_estimate"])
    photo_url = data.get("photo_url")

    if count_estimate < 0:
        return jsonify({"error": "count_estimate must be >= 0"}), 400

    # if no date is sent, use today's date in ISO format
    observed_date = data.get("observed_date")
    if not observed_date:
        observed_date = date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()

    # insert the new sighting row
    cur.execute("""
        INSERT INTO sighting (
            observed_date,
            count_estimate,
            photo_url,
            invasive_scientific_name,
            region_id
        )
        VALUES (?, ?, ?, ?, ?);
    """, (observed_date, count_estimate, photo_url, invasive_scientific_name, region_id))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    new_sighting = {
        "sighting_id": new_id,
        "observed_date": observed_date,
        "count_estimate": count_estimate,
        "photo_url": photo_url,
        "invasive_scientific_name": invasive_scientific_name,
        "region_id": region_id,
    }

    return jsonify({
        "message": "sighting created",
        "sighting": new_sighting,
    }), 201
# Update a sighting (UPDATE)
@app.route("/api/sightings/<int:sighting_id>", methods=["PUT"])
def update_sighting(sighting_id):
    data = request.get_json()
    if data is None:
        return jsonify({"error": "request body must be json"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Build update query based on what fields are provided
    updates = []
    values = []

    if "count_estimate" in data:
        updates.append("count_estimate = ?")
        values.append(data["count_estimate"])

    if "observed_date" in data:
        updates.append("observed_date = ?")
        values.append(data["observed_date"])

    if "photo_url" in data:
        updates.append("photo_url = ?")
        values.append(data["photo_url"])

    if not updates:
        return jsonify({"error": "no fields to update"}), 400

    # Add the sighting_id to values for WHERE clause
    values.append(sighting_id)
    query = f"UPDATE sighting SET {', '.join(updates)} WHERE sighting_id = ?"

    try:
        cur.execute(query, values)
        conn.commit()
        if cur.rowcount == 0:
            conn.close()
            return jsonify({"error": "sighting not found"}), 404
        conn.close()
        return jsonify({"message": "sighting updated", "sighting_id": sighting_id}), 200
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({"error": str(e)}), 400

# Delete a sighting (DELETE)
@app.route("/api/sightings/<int:sighting_id>", methods=["DELETE"])
def delete_sighting(sighting_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM sighting WHERE sighting_id = ?", (sighting_id,))
        conn.commit()
        if cur.rowcount == 0:
            conn.close()
            return jsonify({"error": "sighting not found"}), 404
        conn.close()
        return jsonify({"message": "sighting deleted", "sighting_id": sighting_id}), 200
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "cannot delete due to foreign key constraint"}), 400
    
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


# Update a project (UPDATE)
@app.route("/api/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    data = request.get_json()
    if data is None:
        return jsonify({"error": "request body must be json"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    updates = []
    values = []

    if "status" in data:
        updates.append("status = ?")
        values.append(data["status"])
    if "budget_spent" in data:
        updates.append("budget_spent = ?")
        values.append(data["budget_spent"])
    if "notes" in data:
        updates.append("notes = ?")
        values.append(data["notes"])

    if not updates:
        return jsonify({"error": "no fields to update"}), 400

    values.append(project_id)
    query = f"UPDATE eradication_project SET {', '.join(updates)} WHERE project_id = ?"

    try:
        cur.execute(query, values)
        conn.commit()
        if cur.rowcount == 0:
            conn.close()
            return jsonify({"error": "project not found"}), 404
        conn.close()
        return jsonify({"message": "project updated", "project_id": project_id}), 200
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({"error": str(e)}), 400

# Delete a project (DELETE)
@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # First delete junction table entries to avoid FK constraint issues
        cur.execute("DELETE FROM method_project WHERE project_id = ?", (project_id,))
        cur.execute("DELETE FROM project_region WHERE project_id = ?", (project_id,))
        cur.execute("DELETE FROM species_project WHERE project_id = ?", (project_id,))

        # Then delete the project itself
        cur.execute("DELETE FROM eradication_project WHERE project_id = ?", (project_id,))
        conn.commit()
        if cur.rowcount == 0:
            conn.close()
            return jsonify({"error": "project not found"}), 404
        conn.close()
        return jsonify({"message": "project deleted", "project_id": project_id}), 200
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({"error": str(e)}), 400

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
# Q2: sightings count by region and risk level (real data)
@app.route("/api/queries/2")
def query_2():
    conn = get_db_connection()
    cur = conn.cursor()

    # join sighting with region and invasive_species, then group by region + risk
    cur.execute("""
        SELECT
            r.region_name AS region,
            i.risk_level AS risk_level,
            COUNT(s.sighting_id) AS sighting_count
        FROM sighting AS s
        JOIN region AS r
            ON s.region_id = r.region_id
        JOIN invasive_species AS i
            ON s.invasive_scientific_name = i.invasive_scientific_name
        GROUP BY r.region_name, i.risk_level
        ORDER BY r.region_name, i.risk_level;
    """)

    rows = cur.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "region": row["region"],
            "risk_level": row["risk_level"],
            "count": row["sighting_count"],
        })

    return jsonify(data)

# Q3: projects that use 'Manual Removal' as a control method (real data)
@app.route("/api/queries/3")
def query_3():
    conn = get_db_connection()
    cur = conn.cursor()

    # find projects that are linked to the Manual Removal method
    cur.execute("""
        SELECT
            p.project_id,
            p.name_of_project,
            p.status,
            mp.method_name
        FROM eradication_project AS p
        JOIN method_project AS mp
            ON p.project_id = mp.project_id
        WHERE mp.method_name = 'Manual Removal'
        ORDER BY p.project_id;
    """)

    rows = cur.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "project_id": row["project_id"],
            "name_of_project": row["name_of_project"],
            "status": row["status"],
            "method_name": row["method_name"],
        })

    return jsonify(data)

# Q4: regions with sightings but no active projects (real data)
@app.route("/api/queries/4")
def query_4():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT r.region_id, r.region_name
        FROM region AS r
        JOIN sighting AS s
            ON r.region_id = s.region_id
        WHERE r.region_id NOT IN (
            SELECT pr.region_id
            FROM project_region AS pr
            JOIN eradication_project AS ep
                ON pr.project_id = ep.project_id
            WHERE ep.status = 'active'
        )
        ORDER BY r.region_id;
    """)

    rows = cur.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "region_id": row["region_id"],
            "region_name": row["region_name"]
        })

    return jsonify(data)

# Q5: native species impacted by high risk invasives (real data)
@app.route("/api/queries/5")
def query_5():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            n.scientific_name AS native_scientific_name,
            n.common_name    AS native_common_name,
            COUNT(*)         AS threat_count
        FROM native_species AS n
        JOIN impact AS im
            ON n.scientific_name = im.scientific_name
        JOIN invasive_species AS inv
            ON im.invasive_scientific_name = inv.invasive_scientific_name
        WHERE inv.risk_level = 'high'
        GROUP BY n.scientific_name, n.common_name
        ORDER BY threat_count DESC, n.common_name;
    """)

    rows = cur.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "native_scientific_name": row["native_scientific_name"],
            "native_common_name": row["native_common_name"],
            "threat_count": row["threat_count"],
        })

    return jsonify(data)
# Q6: population trend (sightings count by year) for one invasive species (real data)
@app.route("/api/queries/6")
def query_6():
    # Get species from query string, use default if not given
    species_name = request.args.get("species", "Carcinus maenas")

    conn = get_db_connection()
    cur = conn.cursor()

    # Group sightings by year for the selected species
    cur.execute("""
        SELECT
            strftime('%Y', observed_date) AS year,
            COUNT(*) AS total_sightings
        FROM sighting
        WHERE invasive_scientific_name = ?
        GROUP BY year
        ORDER BY year;
    """, (species_name,))

    rows = cur.fetchall()
    conn.close()

    trend = []
    for row in rows:
        trend.append({
            "year": row["year"],
            "total_sightings": row["total_sightings"],
        })

    return jsonify({
        "invasive_scientific_name": species_name,
        "trend": trend,
    })


if __name__ == "__main__":
    app.run(debug=True)
