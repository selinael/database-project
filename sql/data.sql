
-- REGIONS

INSERT INTO region (region_name, nl_zone) VALUES
('Avalon Peninsula', 'Eastern'),
('Burin Peninsula', 'Southern'),
('Central Newfoundland', 'Central'),
('Northern Peninsula', 'Northern'),
('St. John''s', 'Eastern'),
('Gros Morne', 'Western');



-- INVASIVE SPECIES

INSERT INTO invasive_species (invasive_scientific_name, common_name, kingdom, risk_level, spread_rate, first_record_in_nl) VALUES
('Fallopia japonica', 'Japanese Knotweed', 'Plantae', 'high', 3.1, '2012-06-01'),
('Hemigrapsus sanguineus', 'Asian Shore Crab', 'Animalia', 'medium', 1.8, '2015-08-10'),
('Ciona intestinalis', 'Vase Tunicate', 'Animalia', 'high', 4.0, '2008-09-14'),
('Carcinus maenas', 'European Green Crab', 'Animalia', 'high', 5.2, '2007-07-20'),
('Phragmites australis', 'Common Reed', 'Plantae', 'medium', 2.0, '2013-05-05'),
('Lythrum salicaria', 'Purple Loosestrife', 'Plantae', 'low', 0.5, '2011-04-22');



-- NATIVE SPECIES

INSERT INTO native_species (scientific_name, common_name, conservation_status) VALUES
('Rangifer tarandus', 'Caribou', 'Threatened'),
('Tamiasciurus hudsonicus', 'Red Squirrel', 'Least Concern'),
('Lutra canadensis', 'River Otter', 'Least Concern'),
('Falco columbarius', 'Merlin', 'Least Concern'),
('Salmo salar', 'Atlantic Salmon', 'Endangered');
