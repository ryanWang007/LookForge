"""My Closet routes."""

import sqlite3
from pathlib import Path

from flask import Blueprint, abort, current_app, redirect, render_template, url_for

from db import get_db

closet_bp = Blueprint("closet", __name__)

CATEGORIES = ["Shirts", "Pants", "Dresses", "Jackets", "Shoes", "Other"]
SEASONS = ["Spring", "Summer", "Fall", "Winter"]
COLORS = ["Black", "White", "Gray", "Blue", "Red", "Green", "Brown", "Other"]


@closet_bp.get("/closet")
def index():
    """Show clothing items saved in the database."""
    clothing_items = get_db().execute(
        "SELECT id, name, category, color, season, photo_filename "
        "FROM clothing ORDER BY created_at DESC, id DESC"
    ).fetchall()
    return render_template(
        "closet.html",
        clothing_items=clothing_items,
        categories=CATEGORIES,
        seasons=SEASONS,
        colors=COLORS,
    )


@closet_bp.post("/closet/<int:item_id>/delete")
def delete_item(item_id):
    """Delete a clothing item and its uploaded photo, if any."""
    db = get_db()
    item = db.execute(
        "SELECT photo_filename FROM clothing WHERE id = ?", (item_id,)
    ).fetchone()
    if item is None:
        abort(404)
    
    try:
        db.execute("DELETE FROM clothing WHERE id = ?", (item_id,))
        db.commit()
    except sqlite3.Error:
        db.rollback()
        current_app.logger.exception("Could not delete clothing item %s", item_id)
        abort(500, description="Could not delete clothing item. Please try again.")
    
    # Delete the uploaded photo file if it exists
    photo_filename = item["photo_filename"]
    if photo_filename:
        upload_folder = Path(current_app.config["UPLOAD_FOLDER"]).resolve()
        photo_path = (upload_folder / photo_filename).resolve()
        if photo_path.parent != upload_folder:
            current_app.logger.error(
                "Refusing to delete photo outside upload folder for clothing item %s",
                item_id,
            )
            return redirect(url_for("closet.index", photo_cleanup_error=1))
        try:
            photo_path.unlink(missing_ok=True)
        except OSError:
            current_app.logger.exception(
                "Could not delete photo for clothing item %s", item_id
            )
            return redirect(url_for("closet.index", photo_cleanup_error=1))

    return redirect(url_for("closet.index"))
