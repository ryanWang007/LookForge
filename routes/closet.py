"""My Closet routes."""

from flask import Blueprint, render_template

from db import get_db

closet_bp = Blueprint("closet", __name__)


@closet_bp.get("/closet")
def index():
    """Show clothing items saved in the database."""
    clothing_items = get_db().execute(
        "SELECT id, name, category, color, season, photo_filename "
        "FROM clothing ORDER BY created_at DESC, id DESC"
    ).fetchall()
    return render_template("closet.html", clothing_items=clothing_items)
