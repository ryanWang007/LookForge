-- Starter schema for LookForge. The team can evolve these fields as features grow.
-- This script is safe to run repeatedly on an existing database.

CREATE TABLE IF NOT EXISTS clothing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    color TEXT,
    season TEXT,
    photo_filename TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS looks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS look_items (
    look_id INTEGER NOT NULL,
    clothing_id INTEGER NOT NULL,
    PRIMARY KEY (look_id, clothing_id),
    FOREIGN KEY (look_id) REFERENCES looks(id) ON DELETE CASCADE,
    FOREIGN KEY (clothing_id) REFERENCES clothing(id) ON DELETE CASCADE
);
