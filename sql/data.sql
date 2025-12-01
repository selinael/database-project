
-- REGIONS

INSERT INTO Region (region_name, description) VALUES
('Avalon Peninsula', 'Coastal region with cliffs and protected seabird areas.'),
('Central Newfoundland', 'Forested interior, mixed boreal ecosystems.'),
('Northern Coast', 'Cold marine climate with rugged terrain.'),
('Western Newfoundland', 'Mountainous region with national parks.'),
('Labrador Coast', 'Remote and sparsely populated coastal area.');


-- INVASIVE SPECIES

INSERT INTO InvasiveSpecies (species_name, threat_level, description) VALUES
('Green Crab', 'High', 'Aggressive crab species damaging eelgrass beds.'),
('Japanese Knotweed', 'High', 'Fast-growing plant that destroys soil structure.'),
('European Starling', 'Medium', 'Competes with native birds and disrupts nesting.'),
('Purple Loosestrife', 'Medium', 'Invasive wetland plant spreading rapidly.'),
('Rusty Crayfish', 'High', 'Displaces native crayfish and disrupts freshwater habitats.'),
('Feral Pigs', 'Severe', 'Highly destructive to land and wildlife. Rare but dangerous.');


-- NATIVE SPECIES

INSERT INTO native_species (scientific_name, common_name, conservation_status) VALUES
('Rangifer tarandus', 'Caribou', 'Threatened'),
('Tamiasciurus hudsonicus', 'Red Squirrel', 'Least Concern'),
('Lutra canadensis', 'River Otter', 'Least Concern'),
('Falco columbarius', 'Merlin', 'Least Concern'),
('Salmo salar', 'Atlantic Salmon', 'Endangered');
