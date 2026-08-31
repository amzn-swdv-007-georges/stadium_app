-- Stadium Security HQ — Championship Game Seed Data
-- Night of the championship game: entries from 12:00 to 21:00
-- This is the data that was lost when the server crashed at halftime.
-- Run: sqlite3 stadium.db < seed.sql

DROP TABLE IF EXISTS stadium_entries;
DROP TABLE IF EXISTS people;

CREATE TABLE people (
    id      INTEGER PRIMARY KEY,
    name    TEXT    NOT NULL,
    phone   TEXT    NOT NULL
);

CREATE TABLE stadium_entries (
    id          INTEGER PRIMARY KEY,
    person_id   INTEGER NOT NULL,
    gate        TEXT    NOT NULL,
    hour        INTEGER NOT NULL,
    bag         TEXT    NOT NULL,
    FOREIGN KEY (person_id) REFERENCES people(id)
);

INSERT INTO people (id, name, phone) VALUES
(1,  'Marcus Vance',     '555-0142'),
(2,  'Elena Rostova',    '555-0189'),
(3,  'David Chen',       '555-0123'),
(4,  'Sarah Jenkins',    '555-0199'),
(5,  'Jamal Malik',      '555-0155'),
(6,  'Fiona Gallagher',  '555-0177'),
(7,  'Arthur Pendelton', '555-0131'),
(8,  'Beatrice Vane',    '555-0164'),
(9,  'Carlos Mendez',    '555-0112'),
(10, 'Diana Prince',     '555-0108'),
(11, 'Ethan Hunt',       '555-0147'),
(12, 'Grace Hopper',     '555-0191'),
(13, 'Henry Cavill',     '555-0135'),
(14, 'Ivy League',       '555-0162'),
(15, 'Jack Reacher',     '555-0128'),
(16, 'Karen Page',       '555-0184'),
-- The missing girl and her mother — the case that started everything
(17, 'Rosa Delgado',     '555-0201'),
(18, 'Lucia Delgado',    '555-0201');

INSERT INTO stadium_entries (id, person_id, gate, hour, bag) VALUES
-- Pre-game arrivals (hours 12–14)
(1,  1,  'A', 12, 'none'),
(2,  9,  'A', 11, 'bag'),
(3,  3,  'A', 14, 'backpack'),
(4,  4,  'A', 14, 'bag'),
(5,  7,  'B', 13, 'none'),
(6,  2,  'B', 14, 'bag'),
(7,  14, 'B', 14, 'tote'),
(8,  5,  'C', 14, 'bag'),
(9,  11, 'C', 12, 'none'),
(10, 16, 'C', 14, 'bag'),
(11, 8,  'D', 14, 'purse'),
(12, 13, 'D', 15, 'bag'),
-- Halftime arrivals (hour 15) — last records before the crash
(13, 6,  'A', 15, 'bag'),
(14, 12, 'A', 14, 'none'),
(15, 10, 'B', 16, 'backpack'),
(16, 15, 'A', 17, 'backpack'),
-- Rosa and Lucia Delgado — entered together at Gate C, hour 14
-- Rosa was reported missing after the game
(17, 17, 'C', 14, 'backpack'),
(18, 18, 'C', 14, 'none'),
-- Late-game entries (hours 17–19)
(19, 1,  'A', 19, 'bag'),
(20, 3,  'B', 18, 'none'),
(21, 5,  'A', 17, 'bag'),
(22, 9,  'D', 19, 'backpack');
