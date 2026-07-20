# ARGUS — Secure Code Review Platform

ARGUS is a Django-based static application security testing (SAST) platform.
Upload code four different ways, run it through three complementary scan
engines, and get an interactive dashboard plus an audit-ready PDF report.

## Tech stack → feature mapping

| Technology | Where it's used |
|---|---|
| **Python 3.12 / Django 5** | Core web app, ORM, forms, views, admin |
| **HTML5 / CSS3** | Templates (`templates/`), custom dark theme (`static/css/custom.css`) |
| **JavaScript** | Chart.js wiring, Motion animations (`static/js/animations.js`) |
| **Bootstrap 5** | Layout, components, responsive grid |
| **SQLite / PostgreSQL** | Default dev DB is SQLite; set `ARGUS_DB_ENGINE=postgres` for Postgres |
| **Bandit** | Python-specific security linter (`scanner/engines/bandit_engine.py`) |
| **Semgrep** | Multi-language pattern-based rules engine (`scanner/engines/semgrep_engine.py`) |
| **Python `ast` module** | Custom hand-written rule engine, no third-party dependency (`scanner/engines/ast_engine.py`) |
| **ReportLab** | PDF report generation (`reports/pdf_generator.py`) |
| **Chart.js** | Interactive charts in the web dashboard/scan detail pages |
| **Matplotlib** | Static chart images embedded into the PDF report |
| **Git / GitHub** | Version control (see below); also the "scan a GitHub repo" ingestion path |
| **Motion (formerly Framer Motion)** | Vanilla-JS UI animations, loaded via CDN in `base.html` |

> Note on visualization: the live dashboard renders **Chart.js** (interactive,
> client-side). PDF reports are static documents, so they embed **Matplotlib**
> PNG charts instead — Chart.js can't render server-side without a headless
> browser, and Matplotlib is a much lighter dependency for that job.

## Features

- **Four ways to submit code**: single `.py` file upload, `.zip` project
  archive upload, paste-in-browser snippet, or a GitHub repository URL
  (shallow-cloned automatically).
- **Three scan engines**, each toggleable per scan:
  - **Bandit** — Python-specific security issues (hardcoded passwords, SQL
    injection, insecure crypto, etc.)
  - **Semgrep** — broader, pattern-based static analysis with its default
    `auto` ruleset.
  - **ARGUS AST Engine** — a from-scratch scanner built directly on Python's
    `ast` module. It detects `eval`/`exec`, `os.system`/`shell=True`, insecure
    deserialization (`pickle`, unsafe `yaml.load`), weak hashes (MD5/SHA-1),
    hardcoded secrets, `assert`-based access checks, and SQL built via string
    concatenation. It's intentionally dependency-free and easy to extend —
    see `scanner/engines/ast_engine.py`.
- **Unified findings model**: all three engines' output is normalized into a
  single `Finding` table (severity, CWE, file/line, snippet, remediation).
- **Dashboard & scan detail pages** with Chart.js severity/engine breakdowns
  and a computed 0–100 risk score.
- **PDF reports** (ReportLab) with a cover page, executive summary (risk
  gauge + charts + top findings table), and an optional full technical
  appendix with code snippets and remediation guidance per finding.
- Single-user, no login required — everything runs locally against SQLite by
  default.

## Getting started

```bash
# 1. Clone / unzip this project, then from the project root:
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

# 2. Set up the database
python manage.py migrate

# 3. (optional) create an admin user for /admin/
python manage.py createsuperuser

# 4. Run the dev server
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

### Using PostgreSQL instead of SQLite

```bash
export ARGUS_DB_ENGINE=postgres
export ARGUS_DB_NAME=argus
export ARGUS_DB_USER=argus
export ARGUS_DB_PASSWORD=yourpassword
export ARGUS_DB_HOST=localhost
export ARGUS_DB_PORT=5432
pip install psycopg2-binary
python manage.py migrate
```

### Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `ARGUS_SECRET_KEY` | insecure dev key | Django `SECRET_KEY` — set a real one in production |
| `ARGUS_DEBUG` | `True` | Set to `False` in production |
| `ARGUS_ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated allowed hosts |
| `ARGUS_DB_ENGINE` | sqlite | Set to `postgres` to use PostgreSQL |
| `ARGUS_MAX_ZIP_SIZE` | 25MB | Max upload size for `.zip` archives |
| `ARGUS_SCAN_TIMEOUT` | 120 | Timeout (seconds) for Bandit/Semgrep subprocesses |

## Project structure

```
argus_platform/
├── argus_platform/        # Django project (settings, urls, wsgi)
├── scanner/                # Ingestion + scan orchestration
│   ├── engines/
│   │   ├── ast_engine.py       # Custom Python ast-module scanner
│   │   ├── bandit_engine.py    # Bandit subprocess wrapper
│   │   └── semgrep_engine.py   # Semgrep subprocess wrapper
│   ├── services.py         # Ingestion (file/zip/paste/github) + scan runner
│   ├── models.py           # ScanProject, Finding
│   ├── forms.py / views.py / urls.py
├── reports/                 # PDF generation
│   ├── chart_generator.py  # Matplotlib chart images
│   ├── pdf_generator.py    # ReportLab report builder
│   ├── models.py            # GeneratedReport
├── templates/                # HTML5 + Bootstrap 5 templates
├── static/css/custom.css    # Dark theme
├── static/js/animations.js  # Motion-powered UI animations
└── requirements.txt
```

## Pushing to GitHub

This project is already a local git repository with an initial commit. To
push it to GitHub:

```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

## Security notes

- This tool executes `bandit`/`semgrep` as subprocesses and clones
  repositories with `git`. Only scan code and repositories you trust — static
  analysis tools themselves are not a sandbox.
- ZIP extraction is guarded against path-traversal ("zip-slip"), but you
  should still only upload archives from trusted sources.
- This is a single-user local tool by design (no authentication). If you
  deploy it somewhere reachable over a network, put it behind your own
  authentication layer first.
