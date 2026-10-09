# LookForge

**Tech stack:** Python · Flask · Jinja2 (HTML templates) · SQLite · CSS · Ruff

## Project status
 The repository currently provides:

- A runnable Flask app and three registered **Blueprints** (one backend module per page， you can find it in the routes).
- Three placeholder HTML pages and a shared Jinja2 layout/navigation.
- SQLite connection helpers and an initial database schema.
- Shared starter CSS and Ruff linting configuration.

**Not implemented yet:** each of us should responsible for each frontend(html file) plus a backend(routs.py file).

Rui: **Add Clothing** + initial project setup | `routes/add_clothing.py` | `templates/add_clothing.html

David:  **My Looks** | `routes/looks.py` | `templates/looks.html` 

Jonathan: **My Closet** | `routes/closet.py` | `templates/closet.html` 

### Shared foundation

| File | Purpose |
| --- | --- |
| `app.py` | Creates the Flask app, registers the three Blueprints, redirects `/` to My Closet |
| `db.py` | SQLite connections and database initialization; feature code can use `get_db()` |
| `schema.sql` | Starter database structure for clothing and outfits |
| `routes/__init__.py` | Marks `routes/` as a Python package; no feature logic needed here |
| `templates/base.html` | Shared navigation and Jinja2 template structure |
| `static/css/style.css` | Shared baseline styling |
| `pyproject.toml` | Ruff configuration |

## Project structure

```text
LookForge/
├── app.py
├── db.py
├── schema.sql
├── routes/
│   ├── __init__.py
│   ├── add_clothing.py
│   ├── closet.py
│   └── looks.py
├── templates/
│   ├── base.html
│   ├── add_clothing.html
│   ├── closet.html
│   └── looks.html
├── static/
│   └── css/
│       └── style.css
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

`instance/lookforge.db` is generated **locally** on first run. A future `static/uploads/` folder can store uploaded photos locally; neither generated database files nor uploaded photos should be committed to Git.

## Get started

### 1. Clone the private repository

After accepting the GitHub collaborator invitation:

```bash
git clone https://github.com/ryanWang007/LookForge.git
cd LookForge
```

If you already cloned the project, open the local LookForge folder in VS Code and run `git pull --ff-only origin main` on a clean `main` branch to get the latest foundation.

### 2. Install dependencies and start Flask

**Windows (VS Code PowerShell terminal)**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe app.py
```

If `py` is unavailable, try `python -m venv .venv`.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

Open **http://127.0.0.1:5000**. Flask runs locally; stop it with `Ctrl+C`.

### 3. Check the three placeholder pages

| Page | URL | Blueprint endpoint |
| --- | --- | --- |
| My Closet | `/closet` | `closet.index` |
| My Looks | `/looks` | `looks.index` |
| Add Clothing | `/add-clothing` | `add_clothing.index` |

Each module in `routes/` handles its own URL, and its HTML template extends `templates/base.html`. For example, the shared navigation uses `url_for('looks.index')`.

## SQLite and photo storage

The app creates `instance/lookforge.db` automatically from `schema.sql` when started. The **starter tables** are:

- `clothing` — clothing ID, name, category, color, season, photo filename, created date.
- `looks` — outfit/Look ID, name, created date.
- `look_items` — association between Looks and clothing items.

Access SQLite from Flask feature code with `from db import get_db`. Database connections enable foreign-key checks.

**Planned photo approach (not yet implemented):** Save actual JPG/PNG files under `static/uploads/`, and store the saved **filename** in the `clothing.photo_filename` database field. The ID in `clothing` identifies a clothing record, not a separate image record.

Local SQLite records and uploaded photos **do not sync between teammates through GitHub**. Each person has their own test data. Changing `schema.sql` does not automatically alter tables in an existing database; coordinate schema changes and migrations before relying on them.

## GitHub workflow

1. Start from the latest `main`, and create a **feature branch**:
   - Add Clothing: `feature/add-clothing`
   - My Looks (David): `feature/my-looks`
   - My Closet (Jonathan): `feature/my-closet`
2. Implement and test your own feature locally.
3. Run Ruff before pushing:
   - Windows: `.\.venv\Scripts\python.exe -m ruff check .`
   - macOS / Linux (activated environment): `ruff check .`
4. Push the branch and open a **Pull Request (PR)** targeting `main`.
5. Ask **at least one other team member** to review and approve it before merging. Avoid direct pushes to `main`.

**Note:** GitHub Free with a private repository allows PR reviews, but does not enforce required approvals through branch protection. Following this review policy is our team agreement.

For shared files (`schema.sql`, `db.py`, `app.py`, `templates/base.html`, and `static/css/style.css`), communicate planned changes so another person's work is not broken.

## Next development steps

- **Add Clothing:** implement the form, file validation/upload, and saving a clothing record.
- **My Closet:** read saved clothing from SQLite, display items/photos, and support edit/delete.
- **My Looks:** select existing clothing items and save/view outfit combinations.

Keep the initial implementation simple and localhost-first. We can refine the schema and UI together as the features develop.
