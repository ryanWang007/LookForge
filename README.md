# LookForge

LookForge is a small virtual closet and outfit organizer built with **Python**, **Flask**, **Jinja2**, and **SQLite** for our CS467 team project.

## Current status

This repository contains the **project foundation only**:
- Flask app entry point registering three separate route Blueprints (`/closet`, `/looks`, `/add-clothing`)
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

## Feature ownership (Flask Blueprints)

Each team member can edit one **backend route module** and its matching **Jinja2 template**:

| Feature | Backend | Frontend | Blueprint endpoint |
| --- | --- | --- | --- |
| My Closet | `routes/closet.py` | `templates/closet.html` | `closet.index` |
| My Looks | `routes/looks.py` | `templates/looks.html` | `looks.index` |
| Add Clothing | `routes/add_clothing.py` | `templates/add_clothing.html` | `add_clothing.index` |

`app.py` only creates the Flask app and registers Blueprints; keep feature-specific logic out of it. Routes use `render_template(...)` for now. The shared navigation in `templates/base.html` uses Flask endpoints such as `url_for('closet.index')`.

For database access, use the shared `get_db()` function from `db.py`. `schema.sql` is a shared **starter** schema; coordinate any changes to the tables. There is **no form handling, upload logic, or CRUD yet**.

Uploaded photos, if implemented later, should be saved locally and never committed to GitHub. The `static/uploads/` directory is in `.gitignore`.

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
  routes/
    __init__.py
    closet.py
    looks.py
    add_clothing.py
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
