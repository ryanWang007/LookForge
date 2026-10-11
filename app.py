"""LookForge Flask application init app."""

from pathlib import Path

from flask import Flask, redirect, url_for

from db import init_app as init_database
from routes.add_clothing import add_clothing_bp
from routes.closet import closet_bp
from routes.looks import looks_bp


def create_app():
    """Create the app and register its three feature blueprints."""
    app = Flask(__name__, instance_relative_config=True)
    app.config["DATABASE"] = str(Path(app.instance_path) / "lookforge.db")
    init_database(app)

    app.register_blueprint(closet_bp)
    app.register_blueprint(looks_bp)
    app.register_blueprint(add_clothing_bp)

    @app.get("/")
    def index():
        return redirect(url_for("closet.index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
