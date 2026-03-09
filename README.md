# Sorteio Novo

🇧🇷 [Leia em Português](README.pt-br.md)

Automated parking garage lottery system for residential condominiums. Built for **Villa Nova Condomínios** by **XNAP**.

Sorteio Novo manages fair and transparent parking spot assignments across multiple condominium projects, each with its own rules for allocation priorities, accessibility requirements, and paired/double garage handling.

## Tech Stack

- **Backend:** Django 5.0 / Python 3.12
- **Database:** PostgreSQL (Supabase)
- **Server:** Gunicorn + WhiteNoise
- **Deployment:** Docker (multi-stage build) + Traefik reverse proxy
- **Reports:** openpyxl / pandas (Excel), reportlab / WeasyPrint (PDF), qrcode (QR codes)
- **Frontend:** Django templates, Bootstrap 5, AngularJS (select views)

## Features

- **Per-project lottery engine** — each condominium app has its own allocation algorithm with support for PNE (accessibility) priority, double/paired garages, fixed assignments, and subsolo (floor-level) constraints
- **Excel import/export** — generates lottery result spreadsheets from per-project templates
- **QR code lookup** — residents can look up their assigned spot by apartment number
- **Reset & re-run** — lottery results can be cleared and re-drawn
- **Django admin** — full CRUD for apartments, parking spots, and results
- **Production-ready** — Docker + Traefik with TLS, compressed static files, persistent DB connections

## Project Structure

```
setup/                  # Django project config (settings, urls, wsgi)
  static/               # Source static files (JS, CSS, assets)
    assets/modelos/      # Excel templates per condominium
templates/
  sorteio_novo/          # Shared base templates and partials
  {app_name}/            # App-specific templates
{app_name}/              # One Django app per condominium (13 apps)
  models.py              # Apartamento, Vaga, Sorteio (+ variants)
  views.py               # Lottery logic, Excel export, QR code, reset
  urls.py                # App-prefixed URL patterns
  admin.py               # Admin configuration
Dockerfile               # Multi-stage production image
docker-compose.yml       # Gunicorn + Traefik orchestration
entrypoint.sh            # Wait-for-DB, migrate, collectstatic
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (or uncomment the SQLite config in `setup/settings.py` for local dev)

### Installation

```bash
git clone <repo-url>
cd sorteio_novo_django

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Fill in the environment variables (see below)

python manage.py migrate
python manage.py runserver
```

### Docker

```bash
docker compose up --build
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port (default: 5432) |
| `EMAIL_HOST_PASSWORD` | Gmail app password for email sending |

---

Built with AI-assisted development using [Claude Code](https://claude.ai/code)
