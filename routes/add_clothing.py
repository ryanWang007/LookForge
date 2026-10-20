"""Add Clothing routes."""

from flask import Blueprint, render_template, request

add_clothing_bp = Blueprint("add_clothing", __name__)


@add_clothing_bp.route("/add-clothing", methods=["GET", "POST"])
def index():
    """Display the form; submission handling will be added later."""
    if request.method == "POST":
        # TODO: Read clothing information from the form
        # TODO: Validate form data
        # TODO: Save uploaded photo to UPLOAD_FOLDER
        # TODO: Insert clothing item into SQLite
        # TODO: Redirect to My Closet after a successful save
        return render_template("add_clothing.html"), 501

    return render_template("add_clothing.html")
