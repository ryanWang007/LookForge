"""LookForge Flask application entry point."""

from pathlib import Path

from flask import Flask, redirect, render_template, url_for

from db import init_app as init_database


def create_app():
    """Create the app and register the initial routes."""
    app = Flask(__name__, instance_relative_config=True)
    app.config["DATABASE"] = str(Path(app.instance_path) / "lookforge.db")
    init_database(app)

    @app.get("/")
    def index():
        return redirect(url_for("closet"))

    @app.get("/closet")
    def closet():
        return render_template("closet.html")

    @app.get("/looks")
    def looks():
        return render_template("looks.html")

    @app.get("/add-clothing")
    def add_clothing():
        return render_template("add_clothing.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
