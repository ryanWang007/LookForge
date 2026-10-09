"""My Looks routes. Outfit-building logic will be added here."""

from flask import Blueprint, render_template

looks_bp = Blueprint("looks", __name__)


@looks_bp.get("/looks")
def index():
    """Show the placeholder My Looks page."""
    return render_template("looks.html")
