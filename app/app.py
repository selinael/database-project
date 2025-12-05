from flask import Flask, jsonify, request, render_template
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)

# ----------------- DB CONFIG -----------------
# Figure out where the project lives and where the DB file is.
APP_DIR = Path(__file__).resolve().parent          # .../database-project/app
PROJECT_ROOT = APP_DIR.parent                      # .../database-project
DB_PATH = PROJECT_ROOT / "sql" / "database.db"     # we use the DB created by init_db.py


def get_db_connection():
    """
    Open a connection to our SQLite database.
    - row_factory lets us access columns by name instead of index
    - we also turn on foreign keys so constraints actually work
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ----------------- UI ROUTES -----------------

# Root page + /dashboard both serve the same HTML SPA
@app.route("/")
@app.route("/dashboard")
def dashboard():
    # index.html has all our JS and CSS and does the API calls
    return render_template("index.html")


# ----------------- API: STATS (for dashboard cards) -----------------

@app.route("/api/stats")
def stats():
    """
    Return some basic counts for the dashboard:
    - total species
    - total sightings
    - active projects
    - counts of high/medium/low risk species
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM invasive_species;")
    total_species = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sighting;")
    total_sightings = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM eradication_project WHERE status = 'active';")
    active_projects = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM invasive_species WHERE risk_level = 'high';")
    high_risk = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM invasive_species WHERE risk_level = 'medium';")
    medium_risk = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM invasive_species WHERE risk_level = 'low';")
    low_risk = cur.fetchone()[0]

    conn.close()

    return jsonify({
        "total_species": total_species,
        "total_sightings": total_sightings,
        "active_projects": active_projects,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
    })


# quick “ping” route to check that Flask is alive
@app.route("/test")
def test():
    return "test route is working"


# ----------------- API: INVASIVE SPECIES -----------------

@app.route("/api/invasive-species")
def list_invasive_species():
    """
    Return all invasive species with some basic info.
    This is used to populate:
    - Species table
    - The dropdown in the “Report Sighting” form
    """
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



# ----------------- API: SIGHTINGS -----------------

# GET /api/sightings  -> return all sightings with region names
@app.route("/api/sightings", methods=["GET"])
def list_sightings():
    conn = get_db_connection()
    cur = conn.cursor()

    # join sighting with region so we can show "Avalon Peninsula"
    cur.execute("""
        SELECT
            s.sighting_id,
            s.observed_date,
            s.count_estimate,
            s.invasive_scientific_name,
            s.region_id,
            r.region_name
        FROM sighting AS s
        JOIN region AS r
            ON s.region_id = r.region_id
        ORDER BY s.observed_date DESC, s.sighting_id DESC;
    """)

    rows = cur.fetchall()
    conn.close()

    sightings = []
    for row in rows:
        sightings.append({
            "sighting_id": row["sighting_id"],
            "observed_date": row["observed_date"],
            "count_estimate": row["count_estimate"],
            "invasive_scientific_name": row["invasive_scientific_name"],
            "region_id": row["region_id"],
            "region_name": row["region_name"],   # new field we send to frontend
        })

    return jsonify(sightings)

@app.route("/api/sightings", methods=["POST"])
def create_sighting():
    """
    Create a new sighting.
    Expected JSON:
    {
        "invasive_scientific_name": "...",
        "region_id": 1,
        "count_estimate": 5,
        "observed_date": "YYYY-MM-DD"   # optional, we default to today
    }
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "request body must be json"}), 400

    # make sure required fields exist
    required_fields = ["invasive_scientific_name", "region_id", "count_estimate"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400

    invasive_scientific_name = data["invasive_scientific_name"]
    region_id = int(data["region_id"])
    count_estimate = int(data["count_estimate"])

    # simple validation
    if count_estimate < 0:
        return jsonify({"error": "count_estimate must be >= 0"}), 400

    # if front-end didn’t send a date, use today
    observed_date = data.get("observed_date")
    if not observed_date:
        observed_date = date.today().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sighting (
            observed_date,
            count_estimate,
            invasive_scientific_name,
            region_id
        )
        VALUES (?, ?, ?, ?);
    """, (observed_date, count_estimate, invasive_scientific_name, region_id))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    new_sighting = {
        "sighting_id": new_id,
        "observed_date": observed_date,
        "count_estimate": count_estimate,
        "invasive_scientific_name": invasive_scientific_name,
        "region_id": region_id,
    }

    return jsonify({
        "message": "sighting created",
        "sighting": new_sighting,
    }), 201


@app.route("/api/sightings/<int:sighting_id>", methods=["PUT"])
def update_sighting(sighting_id):
    """
    Update a sighting.
    Right now we only allow changing:
    - count_estimate
    - observed_date
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "request body must be json"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    updates = []
    values = []

    if "count_estimate" in data:
        updates.append("count_estimate = ?")
        values.append(data["count_estimate"])

    if "observed_date" in data:
        updates.append("observed_date = ?")
        values.append(data["observed_date"])

    # if nothing is provided, we bail
    if not updates:
        return jsonify({"error": "no fields to update"}), 400

    values.append(sighting_id)
    query = f"UPDATE sighting SET {', '.join(updates)} WHERE sighting_id = ?"

    try:
        cur.execute(query, values)
        conn.commit()
        if cur.rowcount == 0:
            # no row with that ID
            conn.close()
            return jsonify({"error": "sighting not found"}), 404
        conn.close()
        return jsonify({"message": "sighting updated", "sighting_id": sighting_id}), 200
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({"error": str(e)}), 400


@app.route("/api/sightings/<int:sighting_id>", methods=["DELETE"])
def delete_sighting(sighting_id):
    """
    Delete a sighting by ID.
    If no row is deleted -> 404
    """
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


# ----------------- API: PROJECTS -----------------

@app.route("/api/projects")
def list_projects():
    """
    Return all eradication projects.
    Used for the Projects tab table.
    """
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


@app.route("/api/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    """
    Update a project.
    Allowed fields:
    - status
    - budget_spent
    - notes
    """
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


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    """
    Delete a project.
    We first clean up the junction tables so FK constraints don't complain.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # first remove references in junction tables
        cur.execute("DELETE FROM method_project WHERE project_id = ?", (project_id,))
        cur.execute("DELETE FROM project_region WHERE project_id = ?", (project_id,))
        cur.execute("DELETE FROM species_project WHERE project_id = ?", (project_id,))

        # then delete the actual project row
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


# ----------------- API: QUERIES (Q1–Q6) -----------------

@app.route("/api/queries/1")
def query_1():
    """
    Q1: High-risk species that do NOT have any control method assigned.
    """
    conn = get_db_connection()
    cur = conn.cursor()

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


@app.route("/api/queries/2")
def query_2():
    """
    Q2: Sightings count by region and risk level.
    This joins sighting + region + invasive_species and groups.
    """
    conn = get_db_connection()
    cur = conn.cursor()

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


@app.route("/api/queries/3")
def query_3():
    """
    Q3: Projects that use 'Manual Removal' as a control method.
    """
    conn = get_db_connection()
    cur = conn.cursor()

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


@app.route("/api/queries/4")
def query_4():
    """
    Q4: Regions that have sightings but NO active projects.
    """
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


@app.route("/api/queries/5")
def query_5():
    """
    Q5: Native species impacted by high-risk invasive species.
    """
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


@app.route("/api/queries/6")
def query_6():
    """
    Q6: Population trend (number of sightings per year)
        for a given invasive species.
    If ?species= is not passed, we use European Green Crab by default.
    """
    species_name = request.args.get("species", "Carcinus maenas")

    conn = get_db_connection()
    cur = conn.cursor()

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
@app.route("/api/queries/custom", methods=["POST"])
def query_custom():
    """
    Run a read-only custom SQL query.
    - Only allows a single SELECT statement.
    - Used by the 'Run Custom Query' box in the Queries tab.
    """
    data = request.get_json(silent=True) or {}
    sql = (data.get("sql") or "").strip()

    if not sql:
        return jsonify({"error": "No SQL provided"}), 400

    # Basic safety checks: SELECT-only and single statement
    upper = sql.upper().lstrip()
    if not upper.startswith("SELECT"):
        return jsonify({"error": "Only SELECT statements are allowed"}), 400

    # Disallow multiple statements (anything beyond one ';', except maybe a trailing one)
    if ";" in sql[:-1]:
        return jsonify({"error": "Only a single SELECT statement is allowed"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)

        # Grab column names from cursor.description
        columns = [desc[0] for desc in cur.description] if cur.description else []
        raw_rows = cur.fetchall()

        conn.close()

        # Convert to list of dicts so JSON is nice on the frontend
        rows = [dict(zip(columns, row)) for row in raw_rows]

        return jsonify({"rows": rows})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"SQL error: {e}"}), 400

# ----------------- MAIN -----------------
if __name__ == "__main__":
    # debug=True so we can see errors in the browser while developing
    app.run(debug=True)