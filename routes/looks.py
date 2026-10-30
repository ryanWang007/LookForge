"""My Looks routes. Outfit-building logic will be added here."""

from flask import Blueprint, render_template

from db import get_db

looks_bp = Blueprint("looks", __name__)

OCCASIONS = ["Casual", "Formal", "Everyday", "Work", "Party", "Date Night", "Workout", "Travel"]
SEASONS = ["Spring", "Summer", "Fall", "Winter", "All Season"]
WEATHERS = ["Mild Weather", "Cool Weather", "Warm Weather", "Rainy", "Cold", "Snowy", "Hot"]


@looks_bp.get("/looks")
def index():
    """Show all saved Looks."""

    db = get_db()

    # get every look from the database
    looks = db.execute("SELECT * FROM looks ORDER BY created_at DESC").fetchall()

    look_cards = []
    for look in looks:
        # get the clothing items that belong to the look
        items = db.execute(
            "SELECT clothing.* FROM clothing "
            "JOIN look_items ON look_items.clothing_id = clothing.id "
            "WHERE look_items.look_id = ?",
            (look["id"],),
        ).fetchall()

        # put the look and its items together so the page can loop over them
        look_cards.append({"look": look, "items": items})

    return render_template("looks.html", look_cards=look_cards)


@looks_bp.get("/looks/new")

def new():
    """Show the Create Look form."""
    db = get_db()

    # get all the clothing so the user can pick items for the look
    clothing = db.execute("SELECT * FROM clothing ORDER BY category, name").fetchall()

    return render_template(
        "look_form.html",
        clothing=clothing,
        occasions=OCCASIONS,
        seasons=SEASONS,
        weathers=WEATHERS,
    )