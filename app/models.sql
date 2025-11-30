-- Table: native_species

CREATE TABLE native_species (
    scientific_name     TEXT PRIMARY KEY,
    common_name         TEXT NOT NULL,
    conservation_status TEXT
);


-- Table: region

CREATE TABLE region (
    region_id    INTEGER PRIMARY KEY,
    region_name  TEXT NOT NULL UNIQUE,
    region_type  TEXT,
    nl_zone      TEXT
);


-- Table: invasive_species

CREATE TABLE invasive_species (
    invasive_scientific_name TEXT PRIMARY KEY,
    common_name              TEXT NOT NULL,
    kingdom                  TEXT,
    risk_level               TEXT CHECK (risk_level IN ('low','medium','high')),
    spread_rate              REAL CHECK (spread_rate >= 0),
    first_record_in_nl       DATE
);


-- Table: sighting

CREATE TABLE sighting (
    sighting_id              INTEGER PRIMARY KEY,
    observed_date            DATE NOT NULL,
    count_estimate           INTEGER CHECK (count_estimate >= 0),
    photo_url                TEXT,
    invasive_scientific_name TEXT NOT NULL,
    region_id                INTEGER NOT NULL,
    FOREIGN KEY (invasive_scientific_name) REFERENCES invasive_species(invasive_scientific_name),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);


-- Table: control_method

CREATE TABLE control_method (
    method_name         TEXT PRIMARY KEY,
    method_type         TEXT,
    cost_estimate       REAL CHECK (cost_estimate >= 0),
    description         TEXT,
    effectiveness_range TEXT
);


-- Table: habitat

CREATE TABLE habitat (
    habitat_name TEXT PRIMARY KEY,
    type         TEXT,
    description  TEXT
);


-- Table: eradication_project

CREATE TABLE eradication_project (
    project_id        INTEGER PRIMARY KEY,
    name_of_project   TEXT NOT NULL,
    objective         TEXT,
    status            TEXT CHECK (status IN ('planning','active','completed','on-hold')),
    start_date        DATE,
    end_date          DATE,
    lead_organization TEXT,
    budget_planned    REAL CHECK (budget_planned >= 0),
    budget_spent      REAL CHECK (budget_spent >= 0),
    notes             TEXT
);


-- Table: yearly_status

CREATE TABLE yearly_status (
    status_id                INTEGER PRIMARY KEY,
    presence                 INTEGER CHECK (presence IN (0,1)),
    population               INTEGER CHECK (population >= 0),
    year                     INTEGER NOT NULL,
    invasive_scientific_name TEXT NOT NULL,
    region_id                INTEGER NOT NULL,
    FOREIGN KEY (invasive_scientific_name) REFERENCES invasive_species(invasive_scientific_name),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);


-- Table: species_control_method

CREATE TABLE species_control_method (
    invasive_scientific_name TEXT NOT NULL,
    method_name              TEXT NOT NULL,
    PRIMARY KEY (invasive_scientific_name, method_name),
    FOREIGN KEY (invasive_scientific_name) REFERENCES invasive_species(invasive_scientific_name),
    FOREIGN KEY (method_name) REFERENCES control_method(method_name)
);


-- Table: species_habitat

CREATE TABLE species_habitat (
    invasive_scientific_name TEXT NOT NULL,
    habitat_name             TEXT NOT NULL,
    PRIMARY KEY (invasive_scientific_name, habitat_name),
    FOREIGN KEY (invasive_scientific_name) REFERENCES invasive_species(invasive_scientific_name),
    FOREIGN KEY (habitat_name) REFERENCES habitat(habitat_name)
);


-- Table: method_project

CREATE TABLE method_project (
    project_id  INTEGER NOT NULL,
    method_name TEXT NOT NULL,
    PRIMARY KEY (project_id, method_name),
    FOREIGN KEY (project_id) REFERENCES eradication_project(project_id),
    FOREIGN KEY (method_name) REFERENCES control_method(method_name)
);


-- Table: species_region

CREATE TABLE species_region (
    invasive_scientific_name TEXT NOT NULL,
    region_id                INTEGER NOT NULL,
    PRIMARY KEY (invasive_scientific_name, region_id),
    FOREIGN KEY (invasive_scientific_name) REFERENCES invasive_species(invasive_scientific_name),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);


-- Table: impact

CREATE TABLE impact (
    invasive_scientific_name TEXT NOT NULL,
    scientific_name          TEXT NOT NULL,
    PRIMARY KEY (invasive_scientific_name, scientific_name),
    FOREIGN KEY (invasive_scientific_name) REFERENCES invasive_species(invasive_scientific_name),
    FOREIGN KEY (scientific_name) REFERENCES native_species(scientific_name)
);


-- Table: region_habitat

CREATE TABLE region_habitat (
    habitat_name TEXT NOT NULL,
    region_id    INTEGER NOT NULL,
    PRIMARY KEY (habitat_name, region_id),
    FOREIGN KEY (habitat_name) REFERENCES habitat(habitat_name),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);


-- Table: project_region

CREATE TABLE project_region (
    project_id INTEGER NOT NULL,
    region_id  INTEGER NOT NULL,
    PRIMARY KEY (project_id, region_id),
    FOREIGN KEY (project_id) REFERENCES eradication_project(project_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);


-- Table: species_project

CREATE TABLE species_project (
    invasive_scientific_name TEXT NOT NULL,
    project_id               INTEGER NOT NULL,
    PRIMARY KEY (invasive_scientific_name, project_id),
    FOREIGN KEY (invasive_scientific_name) REFERENCES invasive_species(invasive_scientific_name),
    FOREIGN KEY (project_id) REFERENCES eradication_project(project_id)
);
