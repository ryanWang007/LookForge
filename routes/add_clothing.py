"""Add Clothing page and form handling."""

import sqlite3
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from db import get_db

add_clothing_bp = Blueprint("add_clothing", __name__)

CATEGORIES = {"Shirts", "Pants", "Dresses", "Jacket", "Shoes", "others"}
COLORS = {"Black", "White", "Gray", "Blue", "Red", "Green", "Brown", "Other"}
SEASONS = {"Spring", "Summer", "Fall", "Winter", "All Season"}
MAX_PHOTO_SIZE = 5 * 1024 * 1024


def form_error(message):
    """Show the form again with a validation message."""
    return render_template("add_clothing.html", error=message), 400


@add_clothing_bp.route("/add-clothing", methods=["GET", "POST"])
def index():
    """Show the form or save a new clothing item."""
    if request.method == "GET":
        return render_template("add_clothing.html")

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    color = request.form.get("color", "").strip()
    season = request.form.get("season", "").strip()

    if not all((name, category, color, season)):
        return form_error("Please fill in all clothing details.")
    if len(name) > 100:
        return form_error("Clothing name must be 100 characters or fewer.")
    if category not in CATEGORIES or color not in COLORS or season not in SEASONS:
        return form_error("Please choose options from the dropdown menus.")

    photo = request.files.get("photo")
    saved_path = None
    photo_filename = None

    if photo and photo.filename:
        extension = Path(photo.filename).suffix.lower()
        if extension not in {".jpg", ".jpeg", ".png"}:
            return form_error("Please upload a JPG or PNG photo.")

        # Check the file size and signature, not just the extension.
        photo.stream.seek(0, 2)
        photo_size = photo.stream.tell()
        photo.stream.seek(0)
        if photo_size > MAX_PHOTO_SIZE:
            return form_error("The photo must be 5 MB or smaller.")

        header = photo.stream.read(8)
        photo.stream.seek(0)
        is_png = extension == ".png" and header == b"\x89PNG\r\n\x1a\n"
        is_jpeg = extension in {".jpg", ".jpeg"} and header.startswith(b"\xff\xd8\xff")
        if not (is_png or is_jpeg):
            return form_error("This file is not a valid JPG or PNG photo.")

        photo_filename = f"{uuid4().hex}{'.png' if is_png else '.jpg'}"
        saved_path = Path(current_app.config["UPLOAD_FOLDER"]) / photo_filename

    db = None
    try:
        if saved_path is not None:
            photo.save(saved_path)

        db = get_db()
        db.execute(
            "INSERT INTO clothing (name, category, color, season, photo_filename) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, category, color, season, photo_filename),
        )
        db.commit()
    except (OSError, sqlite3.Error):
        if db is not None:
            db.rollback()
        if saved_path is not None:
            saved_path.unlink(missing_ok=True)
        current_app.logger.exception("Could not save clothing item")
        return render_template(
            "add_clothing.html",
            error="Something went wrong while saving. Please try again.",
        ), 500

    return redirect(url_for("add_clothing.index", saved="1"))
