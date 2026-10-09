"""Add Clothing routes. Form submission and photo upload are TODOs."""

from flask import Blueprint, render_template

add_clothing_bp = Blueprint("add_clothing", __name__)


@add_clothing_bp.get("/add-clothing")
def index():
    """Show the placeholder Add Clothing page (no form handling yet)."""
    return render_template("add_clothing.html")
