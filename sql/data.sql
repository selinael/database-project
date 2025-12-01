
-- REGIONS

INSERT INTO region (region_name, nl_zone) VALUES
('Avalon Peninsula', 'Eastern'),
('Burin Peninsula', 'Southern'),
('Central Newfoundland', 'Central'),
('Northern Peninsula', 'Northern'),
('St. John''s', 'Eastern'),
('Gros Morne', 'Western');



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
