# CLAUDE.md – Software Engineer Moodle (JCT course project)

Instructions for Claude Code (and any AI assistant) working in this repo.
The team is 13 students learning software engineering: explain changes simply, keep code readable, and prefer small steps.

## Architecture (see Wiki: "ייזום מערכתי", chapter 8)
- Distributed Client-Server, one service per business domain (SOA style, not full microservices). REST/JSON between services.
- `frontend/` – React + Vite (port 3000). Each team's screens go in `frontend/src/features/<domain>/`. Service URLs come from `src/api.js` (VITE_* env vars).
- Backend services – Python 3.12 + FastAPI, one Dockerfile each:
  - `backend-core` :8000 – Core & User Management, Roles/Permissions/2FA (epics 32, 36)
  - `backend-courses` :8001 – Course Content & Assignments (epic 33)
  - `backend-ai` :8002 – AI Smart Assistant, Google Gemini (epic 34)
  - `backend-analytics` :8003 – Analytics & Notifications (epic 35)
- Three layers inside every service – keep them separate:
  - `app/api/routes.py` – HTTP only (FastAPI router, request/response models, HTTP errors). Mounted at `/api/<domain>`.
  - `app/services/` – business logic. No HTTP, no direct DB calls.
  - `app/data/` – Supabase access only (`supabase_client.py`: `insert`, `select` via the REST API with httpx).
- A service never reads another service's tables directly; it calls that service's REST API (e.g. `CORE_SERVICE_URL`).
- Database: one shared Supabase (PostgreSQL) project. SQL migrations go in `supabase/NNN_description.sql`, numbered in order, written to be safe to re-run (`if not exists`). Enable RLS on every new table.

## Running
- `docker compose up --build` from the repo root, then http://localhost:3000 (infra-check screen) and http://localhost:800X/docs.
- Hot reload is on: editing files under `backend-*/app` or `frontend/src` applies without rebuilding. Rebuild only after changing `requirements.txt`, `package.json` or a Dockerfile.
- Tests: `cd backend-<service> && python -m pytest -q` (local venv `.venv`), or `docker compose exec backend-<service> pytest -q`.
- Every new endpoint needs at least one pytest test in `backend-<service>/tests/`.

## Git workflow (team rule)
- Each student works only on her personal branch `dev/<name>` and pushes only there.
- Never push to `main`, never force-push. Changes reach `main` only through a Pull Request approved by the sub-team lead and the weekly program lead.
- Before starting work: merge the latest `origin/main` into your branch.
- Commit messages: short, English, mention the Azure work item, e.g. `#209 Add account blocking endpoint`.

## Secrets
- Never read, print, edit or commit `.env`. Keys (SUPABASE_URL, SUPABASE_KEY, GOOGLE_AI_KEY) come only from environment variables. Use the anon key, never `service_role`.
- New config values: add a placeholder to `.env.example` and tell the user to set the real value herself.

## Course documentation
- The course requires documenting AI use: after finishing a task, give the user a short "prompt + review" summary (what was asked, what was generated, what she checked or fixed) to paste into the Azure work item or the Wiki.
