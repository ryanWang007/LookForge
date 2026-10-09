"""Reusable SQLite connection and initialization helpers."""

import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    """Return a database connection for the current request/context."""
    if "db" not in g:
        db = sqlite3.connect(current_app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        g.db = db
    return g.db


def close_db(_exception=None):
    """Close the database connection at the end of a request/context."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the starter tables if they do not exist."""
    with current_app.open_resource("schema.sql") as schema_file:
        get_db().executescript(schema_file.read().decode("utf-8"))
    get_db().commit()


def init_app(app):
    """Register database cleanup and prepare this local instance's database."""
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
