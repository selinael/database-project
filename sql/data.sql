
-- REGIONS

INSERT INTO region (region_name, nl_zone) VALUES
('Avalon Peninsula', 'Eastern'),
('Burin Peninsula', 'Southern'),
('Central Newfoundland', 'Central'),
('Northern Peninsula', 'Northern'),
('St. John''s', 'Eastern'),
('Gros Morne', 'Western');



-- INVASIVE_SPECIES

INSERT INTO invasive_species (invasive_scientific_name, common_name, kingdom, risk_level, spread_rate, first_record_in_nl) VALUES
('Fallopia japonica', 'Japanese Knotweed', 'Plantae', 'high', 3.1, '2012-06-01'),
('Hemigrapsus sanguineus', 'Asian Shore Crab', 'Animalia', 'medium', 1.8, '2015-08-10'),
('Ciona intestinalis', 'Vase Tunicate', 'Animalia', 'high', 4.0, '2008-09-14'),
('Carcinus maenas', 'European Green Crab', 'Animalia', 'high', 5.2, '2007-07-20'),
('Phragmites australis', 'Common Reed', 'Plantae', 'medium', 2.0, '2013-05-05'),
('Lythrum salicaria', 'Purple Loosestrife', 'Plantae', 'low', 0.5, '2011-04-22');



-- NATIVE_SPECIES

INSERT INTO native_species (scientific_name, common_name, conservation_status) VALUES
('Rangifer tarandus', 'Caribou', 'Threatened'),
('Tamiasciurus hudsonicus', 'Red Squirrel', 'Least Concern'),
('Lutra canadensis', 'River Otter', 'Least Concern'),
('Falco columbarius', 'Merlin', 'Least Concern'),
('Salmo salar', 'Atlantic Salmon', 'Endangered');

-- HABITAT

INSERT INTO habitat (habitat_name, type, description) VALUES
('Freshwater Wetlands', 'Wetland', 'Marshes, ponds, low-lying water-logged land'),
('Coastal Shores', 'Coastal', 'Rocky and sandy shoreline zones'),
('Forest Edge', 'Forest', 'Transition zones between forest and open land'),
('Salt Marsh', 'Wetland', 'Coastal wetland influenced by tides'),
('River Estuary', 'Aquatic', 'Brackish water mixing zones'),
('Open Field', 'Grassland', 'Non-forested fields and meadows');

-- CONTROL_METHOD

INSERT INTO control_method (method_name, method_type, cost_estimate, description, effectiveness_range) VALUES
('Manual Removal', 'Physical', 200.00, 'Hand-pulling or digging invasive roots', 'Low-Medium'),
('Herbicide Spray', 'Chemical', 450.00, 'Selective herbicide application', 'Medium-High'),
('Biological Control', 'Biological', 800.00, 'Introducing natural predators', 'Medium'),
('Trapping Program', 'Physical', 300.00, 'Capture and removal traps', 'Low-Medium'),
('Barrier Installation', 'Mechanical', 600.00, 'Physical barriers to restrict spread', 'Medium'),
('Public Awareness Campaign', 'Educational', 150.00, 'Community involvement and education', 'Low');


-- ERADICATION_PROJECT

INSERT INTO eradication_project (name_of_project, objective, status, start_date, end_date, lead_organization, budget_planned, budget_spent, notes) VALUES
('Knotweed Removal 2024', 'Reduce knotweed in Avalon Peninsula', 'active', '2024-04-01', NULL, 'NL Forestry Division', 30000, 12000, 'Good early progress'),
('Green Crab Control Phase 2', 'Population reduction', 'active', '2023-06-15', NULL, 'DFO', 45000, 30000, 'Expanding trapping zones'),
('Loosestrife Survey', 'Determine spread across NL', 'completed', '2022-05-01', '2022-09-20', 'NL Wildlife', 10000, 12500, 'Over budget due to extra fieldwork'),
('Reed Management Program', 'Prevent spread to protected wetlands', 'planning', '2025-01-01', NULL, 'Parks Canada', 50000, 0, 'Initial planning'),
('Crab Impact Study', 'Study ecosystem effects', 'on-hold', '2023-01-10', NULL, 'Memorial University', 20000, 5000, 'Paused due to storms');


-- SPECIES_REGION (JUNCTION TABLE)

INSERT INTO species_region (invasive_scientific_name, region_id) VALUES
('Fallopia japonica', 1),
('Fallopia japonica', 5),
('Carcinus maenas', 2),
('Carcinus maenas', 4),
('Hemigrapsus sanguineus', 6),
('Ciona intestinalis', 6),
('Phragmites australis', 3),
('Lythrum salicaria', 1);


-- SPECIES_HABITAT (JUNCTION TABLE)

INSERT INTO species_habitat (invasive_scientific_name, habitat_name) VALUES
('Fallopia japonica', 'Forest Edge'),
('Fallopia japonica', 'Open Field'),
('Carcinus maenas', 'Coastal Shores'),
('Ciona intestinalis', 'River Estuary'),
('Phragmites australis', 'Freshwater Wetlands'),
('Lythrum salicaria', 'Freshwater Wetlands'),
('Hemigrapsus sanguineus', 'Coastal Shores'),
('Carcinus maenas', 'Salt Marsh');


-- SPECIES_CONTROL_METHOD (JUNCTION TABLE)

INSERT INTO species_control_method (invasive_scientific_name, method_name) VALUES
('Fallopia japonica', 'Manual Removal'),
('Fallopia japonica', 'Herbicide Spray'),
('Carcinus maenas', 'Trapping Program'),
('Carcinus maenas', 'Barrier Installation'),
('Phragmites australis', 'Herbicide Spray'),
('Lythrum salicaria', 'Manual Removal'),
('Ciona intestinalis', 'Biological Control'),
('Hemigrapsus sanguineus', 'Public Awareness Campaign');
