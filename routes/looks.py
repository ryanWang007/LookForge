"""My Looks routes. Outfit-building logic will be added here."""

from flask import Blueprint, render_template

from db import get_db

looks_bp = Blueprint("looks", __name__)


@looks_bp.get("/looks")
def index():
    """Show the placeholder My Looks page."""
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
