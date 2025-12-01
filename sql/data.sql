
-- REGIONS

INSERT INTO region (region_name, nl_zone) VALUES
('Avalon Peninsula', 'Eastern'),
('Burin Peninsula', 'Southern'),
('Central Newfoundland', 'Central'),
('Northern Peninsula', 'Northern'),
('St. John''s', 'Eastern'),
('Gros Morne', 'Western'),
('Labrador Coast', 'Northern'),
('Bonavista Bay', 'Eastern'),
('Lake Melville', 'Northern');



-- INVASIVE_SPECIES

INSERT INTO invasive_species (invasive_scientific_name, common_name, kingdom, risk_level, spread_rate, first_record_in_nl) VALUES
('Fallopia japonica', 'Japanese Knotweed', 'Plantae', 'high', 3.1, '2012-06-01'),
('Hemigrapsus sanguineus', 'Asian Shore Crab', 'Animalia', 'medium', 1.8, '2015-08-10'),
('Ciona intestinalis', 'Vase Tunicate', 'Animalia', 'high', 4.0, '2008-09-14'),
('Carcinus maenas', 'European Green Crab', 'Animalia', 'high', 5.2, '2007-07-20'),
('Phragmites australis', 'Common Reed', 'Plantae', 'medium', 2.0, '2013-05-05'),
('Lythrum salicaria', 'Purple Loosestrife', 'Plantae', 'low', 0.5, '2011-04-22'),
('Didemnum vexillum', 'Marine Carpet Sea Squirt', 'Animalia', 'high', 4.5, '2017-06-18'),
('Elodea canadensis', 'Canadian Waterweed', 'Plantae', 'medium', 1.2, '2019-09-05'),
('Myriophyllum spicatum', 'Eurasian Watermilfoil', 'Plantae', 'high', 3.8, '2019-06-01'),
('Styela clava', 'Club Tunicate', 'Animalia', 'high', 4.2, '2016-09-10'),
('Spartina alterniflora', 'Smooth Cordgrass', 'Plantae', 'high', 2.9, '2014-05-12'),
('Ailanthus altissima', 'Tree-of-heaven', 'Plantae', 'high', 2.5, '2011-03-20'),
('Agrilus planipennis', 'Emerald Ash Borer', 'Animalia', 'high', 5.0, '2017-07-01'),
('Pseudorasbora parva', 'Topmouth Gudgeon', 'Animalia', 'high', 4.6, NULL);


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
('Open Field', 'Grassland', 'Non-forested fields and meadows'),
('Tidal Flats', 'Coastal', 'Intertidal zones with sediment'),
('Deep Marine Zone', 'Aquatic', 'Cold deep-water marine environment');

-- CONTROL_METHOD

INSERT INTO control_method (method_name, method_type, cost_estimate, description, effectiveness_range) VALUES
('Manual Removal', 'Physical', 200.00, 'Hand-pulling or digging invasive roots', 'Low-Medium'),
('Chemical Treatment', 'Chemical', 450.00, 'Selective herbicide application', 'Medium-High'),
('Biological Control', 'Biological', 800.00, 'Introducing natural predators', 'Medium'),
('Trapping Program', 'Physical', 300.00, 'Capture and removal traps', 'Low-Medium'),
('Barrier Installation', 'Mechanical', 600.00, 'Physical barriers to restrict spread', 'Medium'),
('Public Awareness Campaign', 'Educational', 150.00, 'Community involvement and education', 'Low'),
('Hot Water Treatment', 'Physical', 900.00, 'Boiling water flushing for marine organisms', 'Medium-High'),
('Sediment Removal', 'Mechanical', 1100.00, 'Removing top sediment layer to detach tunicates', 'Medium'),
('Early Detection Rapid Response (EDRR)', 'Surveillance', 500.00, 'Ongoing monitoring with a rapid-response team to eradicate new incursions quickly', 'High'),
('Sediment Capping', 'Mechanical', 2500.00, 'Place a clean cap over contaminated sediments to bury benthic invasives', 'Medium'),
('Public Incentive Program', 'Educational', 400.00, 'Grants or incentives to encourage private landowners to remove invasives', 'Low-Medium'),
('Integrated Pest Management', 'Integrated', 1200.00, 'Combines biological, chemical and mechanical techniques tailored to site-specific conditions', 'High'),
('Habitat Restoration', 'Ecological', 2000.00, 'Restore native vegetation and hydrology to reduce habitat suitability for invasives', 'Medium-High'),
('Physical Exclusion', 'Mechanical', 700.00, 'Netting, screening or fencing to prevent movement and establishment of species', 'Medium-High'),
('Quarantine & Biosecurity', 'Policy', 300.00, 'Decontamination and movement controls for boats, equipment, stock and soil', 'High');


-- ERADICATION_PROJECT

INSERT INTO eradication_project (name_of_project, objective, status, start_date, end_date, lead_organization, budget_planned, budget_spent, notes) VALUES
('Knotweed Removal 2024', 'Reduce knotweed in Avalon Peninsula', 'active', '2024-04-01', NULL, 'NL Forestry Division', 30000, 12000, 'Good early progress'),
('Green Crab Control Phase 2', 'Population reduction', 'active', '2023-06-15', NULL, 'DFO', 45000, 30000, 'Expanding trapping zones'),
('Loosestrife Survey', 'Determine spread across NL', 'completed', '2022-05-01', '2022-09-20', 'NL Wildlife', 10000, 12500, 'Over budget due to extra fieldwork'),
('Reed Management Program', 'Prevent spread to protected wetlands', 'planning', '2025-01-01', NULL, 'Parks Canada', 50000, 0, 'Initial planning'),
('Crab Impact Study', 'Study ecosystem effects', 'on-hold', '2023-01-10', NULL, 'Memorial University', 20000, 5000, 'Paused due to storms'),
('Marine Tunicate Response Team', 'Reduce invasive tunicate densities', 'active', '2023-04-10', NULL, 'DFO', 60000, 20000, 'Ongoing marine surveys'),
('Elodea Containment Pilot', 'Limit spread of Elodea in lakes', 'planning', '2025-05-01', NULL, 'NL Environment', 15000, 0, 'Initial containment design'),
('Cordgrass Removal Initiative', 'Control Spartina alterniflora in estuaries', 'active', '2025-03-01', NULL, 'DFO', 40000, 5000, 'Chemical marsh treatment trials'),
('Emerald Ash Borer Mitigation', 'Protect ash stands near communities', 'planning', '2025-06-01', NULL, 'NL Forestry Division', 60000, 0, 'Chemical trunk injections planned'),
('Topmouth Gudgeon Eradication', 'Eradicate Pseudorasbora parva from small lakes', 'active', '2024-09-01', NULL, 'NL Environment', 35000, 12000, 'Rotenone treatments under permit');

-- SPECIES_REGION (JUNCTION TABLE)

INSERT INTO species_region (invasive_scientific_name, region_id) VALUES
('Fallopia japonica', 1),
('Fallopia japonica', 5),
('Carcinus maenas', 2),
('Carcinus maenas', 4),
('Hemigrapsus sanguineus', 6),
('Ciona intestinalis', 6),
('Phragmites australis', 3),
('Lythrum salicaria', 1),
('Didemnum vexillum', 7), 
('Didemnum vexillum', 6),  
('Elodea canadensis', 9),  
('Elodea canadensis', 3);  


-- SPECIES_HABITAT (JUNCTION TABLE)

INSERT INTO species_habitat (invasive_scientific_name, habitat_name) VALUES
('Fallopia japonica', 'Forest Edge'),
('Fallopia japonica', 'Open Field'),
('Carcinus maenas', 'Coastal Shores'),
('Ciona intestinalis', 'River Estuary'),
('Phragmites australis', 'Freshwater Wetlands'),
('Lythrum salicaria', 'Freshwater Wetlands'),
('Hemigrapsus sanguineus', 'Coastal Shores'),
('Carcinus maenas', 'Salt Marsh'),
('Didemnum vexillum', 'Deep Marine Zone'),
('Didemnum vexillum', 'Tidal Flats'),
('Elodea canadensis', 'Freshwater Wetlands');


-- SPECIES_CONTROL_METHOD (JUNCTION TABLE)

INSERT INTO species_control_method (invasive_scientific_name, method_name) VALUES
('Fallopia japonica', 'Manual Removal'),
('Fallopia japonica', 'Chemical Treatment'),
('Carcinus maenas', 'Trapping Program'),
('Carcinus maenas', 'Barrier Installation'),
('Phragmites australis', 'Chemical Treatment'),
('Hemigrapsus sanguineus', 'Public Awareness Campaign'),
('Didemnum vexillum', 'Hot Water Treatment'),


-- IMPACT (JUNCTION TABLE)

INSERT INTO impact (invasive_scientific_name, scientific_name) VALUES
('Carcinus maenas', 'Rangifer tarandus'),
('Carcinus maenas', 'Salmo salar'),
('Fallopia japonica', 'Tamiasciurus hudsonicus'),
('Lythrum salicaria', 'Falco columbarius'),
('Phragmites australis', 'Salmo salar'),
('Ciona intestinalis', 'Lutra canadensis'),
('Didemnum vexillum', 'Salmo salar'),
('Elodea canadensis', 'Lutra canadensis');


-- REGION_HABITAT (JUNCTION TABLE)

INSERT INTO region_habitat (habitat_name, region_id) VALUES
('Coastal Shores', 2),
('Coastal Shores', 4),
('Freshwater Wetlands', 3),
('Freshwater Wetlands', 1),
('Forest Edge', 1),
('Salt Marsh', 6),
('River Estuary', 6),
('Open Field', 5),
('Tidal Flats', 7),  
('Deep Marine Zone', 7),
('Freshwater Wetlands', 9); 

-- PROJECT_REGION (JUNCTION TABLE)

INSERT INTO project_region (project_id, region_id) VALUES
(1, 1),
(1, 5),
(2, 2),
(2, 4),
(4, 3),
(5, 6),
(6, 7),
(6, 6),
(7, 9),
(7, 3);


-- SPECIES_PROJECT (JUNCTION TABLE)

INSERT INTO species_project (invasive_scientific_name, project_id) VALUES
('Fallopia japonica', 1),
('Carcinus maenas', 2),
('Lythrum salicaria', 3),
('Phragmites australis', 4),
('Carcinus maenas', 5),
('Ciona intestinalis', 5),
('Didemnum vexillum', 6),
('Elodea canadensis', 7);


-- METHOD_PROJECT (JUNCTION TABLE)

INSERT INTO method_project (project_id, method_name) VALUES
    (1, 'Manual Removal'),
    (1, 'Chemical Treatment'),

    (2, 'Chemical Treatment'),
    (2, 'Trapping Program'),

    (3, 'Public Awareness Campaign'),

    (4, 'Manual Removal'),
    (4, 'Barrier Installation'),

    (5, 'Biological Control'),
    (5, 'Public Awareness Campaign'),

    (6, 'Hot Water Treatment'),

    (7, 'Manual Removal');

    (8, 'Chemical Treatment'),
    
    (9, 'Chemical Treatment'),
    
    (10, 'Chemical Treatment');



-- SIGHTING

INSERT INTO sighting (observed_date, count_estimate, invasive_scientific_name, region_id) VALUES
('2023-06-01', 15,'Fallopia japonica', 1),
('2022-06-03', 0, 'Fallopia japonica', 5),
('2024-07-10', 42, 'Carcinus maenas', 2),
('2021-07-12', 8, 'Carcinus maenas', 4),
('2024-05-22', 5, 'Ciona intestinalis', 6),
('2024-08-14', 30, 'Hemigrapsus sanguineus', 6),
('2024-05-14', 3, 'Phragmites australis', 3),
('2025-04-20', 2, 'Lythrum salicaria', 1),
('2024-06-19', 60, 'Carcinus maenas', 4),
('2024-08-01', 1,'Fallopia japonica', 1),
('2024-09-12', 200, 'Didemnum vexillum', 7),
('2023-07-21', 540, 'Didemnum vexillum', 6),
('2024-05-11', 12, 'Elodea canadensis', 3),
('2024-06-14', 0, 'Elodea canadensis', 9),
('2023-10-02', 85, 'Carcinus maenas', 7),
('2024-01-19', 1, 'Fallopia japonica', 9);


-- YEARLY_STATUS

INSERT INTO yearly_status (presence, population, year, invasive_scientific_name, region_id) VALUES
(1, 120, 2023, 'Fallopia japonica', 1),
(1, 30, 2024, 'Fallopia japonica', 5),
(1, 800, 2023, 'Carcinus maenas', 2),
(1, 1500, 2024, 'Carcinus maenas', 4),
(1, 300, 2024, 'Hemigrapsus sanguineus', 6),
(1, 5000, 2023, 'Ciona intestinalis', 6),
(1, 50, 2023, 'Phragmites australis', 3),
(1, 12, 2024, 'Lythrum salicaria', 1),
(0, 0, 2022, 'Fallopia japonica', 1),  
(1, 1, 2024, 'Phragmites australis', 3),
(1, 3200, 2023, 'Didemnum vexillum', 7),
(1, 3500, 2024, 'Didemnum vexillum', 7),
(0, 0, 2022, 'Didemnum vexillum', 7),  
(1, 40, 2024, 'Elodea canadensis', 3),
(0, 0, 2023, 'Elodea canadensis', 3),  
(1, 8, 2024, 'Elodea canadensis', 9),
(1, 0, 2020, 'Carcinus maenas', 7);
