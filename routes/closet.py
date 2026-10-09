"""My Closet routes. The clothing-list feature will be built here."""

from flask import Blueprint, render_template

closet_bp = Blueprint("closet", __name__)


@closet_bp.get("/closet")
def index():
    """Show the placeholder My Closet page."""
    return render_template("closet.html")
