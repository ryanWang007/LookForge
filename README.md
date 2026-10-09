# LookForge

LookForge is a small virtual closet and outfit organizer built with **Python**, **Flask**, **Jinja2**, and **SQLite** for our CS467 team project.

## Current status

This repository contains the **project foundation only**:
- Flask app startup and basic routes (`/closet`, `/looks`, `/add-clothing`)
- A shared Jinja2 layout and three placeholder templates
- Local SQLite connection helpers and a starter schema
- Basic shared CSS and Ruff configuration

**Not yet implemented:** Add Clothing form, photo uploads, clothing CRUD, saving/viewing outfits, or final page designs. Those belong to the feature-development phase.

## Run locally (Windows PowerShell)

From the cloned `LookForge` folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000>. The home page redirects to My Closet. Stop the server with `Ctrl+C`.

If `py` is unavailable, use `python -m venv .venv` instead.

## Run locally (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

## Local database

The app automatically creates `instance/lookforge.db` on first run from `schema.sql`. It currently defines `clothing`, `looks`, and `look_items` as **starter** tables. They can be adjusted together as the features are designed. The generated `.db` file and each developer's data are **not tracked by Git**.

Application code can import `get_db` from `db.py` when implementing a feature. Foreign-key enforcement is enabled on these connections.

## Code style

Run `ruff check .` after activating your environment, or run `.\.venv\Scripts\python.exe -m ruff check .` on Windows.

## Team workflow

Please work on your own feature branch and open a pull request into `main`. Ask another teammate to review and approve it before merging. This is a team rule; GitHub Free private repositories do not enforce the approval automatically.

## Project layout

```text
LookForge/
  app.py
  db.py
  schema.sql
  templates/
    base.html
    closet.html
    looks.html
    add_clothing.html
  static/
    css/style.css
  requirements.txt
  requirements-dev.txt
  pyproject.toml
  README.md
```
