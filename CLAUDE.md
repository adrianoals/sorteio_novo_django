# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sorteio Novo is a Django application for Villa Nova Condomínios that automates parking garage lottery assignments for residential condominiums. Each condominium project is its own Django app (13 apps total), all following a similar pattern but with project-specific lottery rules.

## Commands

```bash
# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic --noinput

# Docker build and run
docker compose up --build
```

There are no test suites, linters, or custom management commands configured.

## Architecture

**Django settings module:** `setup.settings`

The `setup/` directory is the Django project root (settings, urls, wsgi, asgi, static files source).

### App Pattern

Each condominium is a separate Django app with the same 3-model structure:

- **Apartamento** — apartment/unit with attributes like PNE (accessibility), priority, block
- **Vaga** — parking spot with attributes like subsolo (floor level), tipo (simple/double)
- **Sorteio** — lottery result linking Apartamento → Vaga with a timestamp

Some apps extend this with extra models (e.g., `DuplaApartamentos`, `SorteioDupla` for paired garage logic in `tres_coelhos`).

### View Pattern

Each app typically has these views:
1. **Sorteio** — executes the random assignment algorithm (POST) or shows results (GET)
2. **Excel export** — generates .xlsx from template files in `setup/static/assets/modelos/`
3. **QR code** — filters results by apartment number
4. **Zerar (reset)** — deletes all Sorteio records for re-running

Lottery logic varies per condominium: some have fixed allocations for specific apartments, PNE-priority handling, subsolo-based allocation, or double-vaga pairing. Session storage is used for passing results between views.

### URL Routing

All apps are included at the root path in `setup/urls.py` (`path('', include('app.urls'))`). Each app prefixes its URLs with its own name (e.g., `sky-view-sorteio/`, `3coelhos-menu/`).

### Templates

- Base templates in `templates/sorteio_novo/` (base.html uses Bootstrap 5.1.3, base_tailwind.html for Tailwind)
- App-specific templates in `templates/{app_name}/`
- Partials in `templates/sorteio_novo/partials/`

### Static Files

- Source: `setup/static/` (assets, js, styles)
- Some apps use AngularJS for dynamic UI
- WhiteNoise serves static files in production with `CompressedManifestStaticFilesStorage`

## Deployment

- **Docker** with `python:3.12-slim` base image
- **Gunicorn** (3 workers, 120s timeout)
- **Traefik** reverse proxy with TLS on domain `sn.sorteionovo.com.br`
- **PostgreSQL** on Supabase (SSL required, connection pooling)
- **entrypoint.sh** waits for DB, runs migrate, collectstatic, then starts gunicorn

## Key Dependencies

- `openpyxl` / `pandas` — Excel generation and data processing
- `reportlab` / `weasyprint` — PDF generation
- `qrcode` / `pillow` — QR code and image generation
- `python-dotenv` — environment variables from `.env`
- `psycopg2-binary` — PostgreSQL adapter

## Language

The codebase, UI, and domain terminology are in **Brazilian Portuguese** (pt-br). Variable names, model fields, and templates use Portuguese.
