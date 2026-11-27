import sqlite3

from flask import Blueprint, abort, redirect, render_template, request, url_for

from db import get_db

looks_bp = Blueprint("looks", __name__)

OCCASIONS = ["Casual", "Formal", "Everyday", "Work", "Party", "Date Night", "Workout", "Travel"]
SEASONS = ["Spring", "Summer", "Fall", "Winter", "All Season"]
WEATHERS = ["Mild Weather", "Cool Weather", "Warm Weather", "Rainy", "Cold", "Snowy", "Hot"]

def get_clothing(db):
    return db.execute("SELECT * FROM clothing ORDER BY category, name").fetchall()

def render_form(db, errors=None, form=None, status=200, look_id=None, selected_ids=None):
    """Render the Look form (create, or edit when look_id is given)."""
    form = form or {}
    if selected_ids is None:
        selected_ids = set(form.getlist("clothing_ids")) if form else set()
    return render_template(
        "look_form.html",
        clothing=get_clothing(db),
        occasions=OCCASIONS,
        seasons=SEASONS,
        weathers=WEATHERS,
        errors=errors or [],
        form=form,
        selected_ids=selected_ids,
        look_id=look_id,
    ), status

def validate_look(db, form):
    """Check the form. Returns (errors, item_ids)."""
    errors = []

    if not form.get("name", "").strip():
        errors.append("Look name is required.")

    for field, allowed in (
        ("occasion", OCCASIONS),
        ("season", SEASONS),
        ("weather", WEATHERS),
    ):
        value = form.get(field, "")
        if value and value not in allowed:
            errors.append(f"Invalid {field}.")

    raw_ids = set(form.getlist("clothing_ids"))
    if not raw_ids:
        errors.append("Pick at least one clothing item.")
        return errors, []

    if not all(r.isdigit() for r in raw_ids):
        errors.append("Invalid clothing item.")
        return errors, []

    item_ids = [int(r) for r in raw_ids]

    marks = ",".join("?" * len(item_ids))
    found = db.execute(
        f"SELECT COUNT(*) FROM clothing WHERE id IN ({marks})", item_ids
    ).fetchone()[0]
    if found != len(item_ids):
        errors.append("One or more clothing items don't exist.")

    return errors, item_ids

@looks_bp.get("/looks")
def index():
    """Show all saved Looks."""
    db = get_db()

    # one query for everything instead of one query per look
    rows = db.execute(
        "SELECT looks.id AS look_id, looks.name AS look_name, looks.occasion, "
        "       looks.season, looks.weather, "
        "       clothing.name AS item_name, clothing.photo_filename "
        "FROM looks "
        "LEFT JOIN look_items ON look_items.look_id = looks.id "
        "LEFT JOIN clothing ON clothing.id = look_items.clothing_id "
        "ORDER BY looks.created_at DESC, looks.id DESC"
    ).fetchall()

    cards = {}
    for row in rows:
        card = cards.setdefault(
            row["look_id"],
            {
                "look": {
                    "id": row["look_id"],
                    "name": row["look_name"],
                    "occasion": row["occasion"],
                    "season": row["season"],
                    "weather": row["weather"],
                },
                "items": [],
            },
        )
        if row["item_name"] is not None:
            card["items"].append(
                {"name": row["item_name"], "photo_filename": row["photo_filename"]}
            )

    return render_template("looks.html", look_cards=list(cards.values()))

@looks_bp.get("/looks/new")
def new():
    """Show the Create Look form."""
    return render_form(get_db())

@looks_bp.post("/looks")
def create():
    """Validate and save a new Look with its clothing items."""
    db = get_db()

    errors, item_ids = validate_look(db, request.form)
    if errors:
        return render_form(db, errors, request.form, 400)

    name = request.form["name"].strip()
    occasion = request.form.get("occasion") or None
    season = request.form.get("season") or None
    weather = request.form.get("weather") or None

    # one transaction so we never save a look with no items
    try:
        cur = db.execute(
            "INSERT INTO looks (name, occasion, season, weather) VALUES (?, ?, ?, ?)",
            (name, occasion, season, weather),
        )
        db.executemany(
            "INSERT INTO look_items (look_id, clothing_id) VALUES (?, ?)",
            [(cur.lastrowid, cid) for cid in item_ids],
        )
        db.commit()
    except sqlite3.Error:
        db.rollback()
        raise

    return redirect(url_for("looks.index"))

@looks_bp.post("/looks/<int:look_id>/delete")
def delete(look_id):
    """Delete a Look. ON DELETE CASCADE removes its look_items rows."""
    db = get_db()

    cur = db.execute("DELETE FROM looks WHERE id = ?", (look_id,))
    db.commit()

    if cur.rowcount == 0:
        abort(404)

    return redirect(url_for("looks.index"))

@looks_bp.get("/looks/<int:look_id>/edit")
def edit(look_id):
    """Show the form filled in with an existing Look."""
    db = get_db()

    look = db.execute("SELECT * FROM looks WHERE id = ?", (look_id,)).fetchone()
    if look is None:
        abort(404)

    rows = db.execute(
        "SELECT clothing_id FROM look_items WHERE look_id = ?", (look_id,)
    ).fetchall()
    selected_ids = {str(r["clothing_id"]) for r in rows}

    return render_form(db, form=dict(look), look_id=look_id, selected_ids=selected_ids)

@looks_bp.post("/looks/<int:look_id>/edit")
def update(look_id):
    """Validate and save changes to an existing Look and its items."""
    db = get_db()

    exists = db.execute("SELECT id FROM looks WHERE id = ?", (look_id,)).fetchone()
    if exists is None:
        abort(404)

    errors, item_ids = validate_look(db, request.form)
    if errors:
        return render_form(db, errors, request.form, 400, look_id=look_id)

    name = request.form["name"].strip()
    occasion = request.form.get("occasion") or None
    season = request.form.get("season") or None
    weather = request.form.get("weather") or None

    try:
        db.execute(
            "UPDATE looks SET name = ?, occasion = ?, season = ?, weather = ? WHERE id = ?",
            (name, occasion, season, weather, look_id),
        )
        db.execute("DELETE FROM look_items WHERE look_id = ?", (look_id,))
        db.executemany(
            "INSERT INTO look_items (look_id, clothing_id) VALUES (?, ?)",
            [(look_id, cid) for cid in item_ids],
        )
        db.commit()
    except sqlite3.Error:
        db.rollback()
        raise

    return redirect(url_for("looks.index"))
