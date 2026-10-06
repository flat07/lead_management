# Mini CRM — Lead Management System

A lightweight CRM built with **Django**, **Tailwind CSS**, and **DaisyUI** for managing sales leads — from creation to conversion. Designed with a clean backend architecture, REST API, and server-rendered UI in a single Django project.

---

## 📌 Overview

Mini CRM allows a small company to capture, track, and manage leads through a simple sales pipeline. Each lead moves through a well-defined status flow (`New → Contacted → Qualified → Won / Lost`), and every change is tracked through an activity log.

The project is intentionally built with **pure Django** (no DRF, no SPA framework) to demonstrate:

- Solid backend architecture and data modeling
- API design using Django's built-in views
- Authentication, validation, pagination, and filtering
- Clean UI with Tailwind CSS + DaisyUI

---

## ✨ Features

### Core

- **Lead CRUD** — create, view, edit, delete leads
- **Lead fields** — `name`, `phone` or `email` (at least one required), `source`, `note`, `status`
- **Lead statuses** — `New`, `Contacted`, `Qualified`, `Won`, `Lost`
- **Lead list** — pagination, search by name/phone/email, filter by status
- **Lead detail** — full information, inline edit, quick status change
- **REST API** — authentication, CRUD, validation, pagination, filtering
- **Error handling** — friendly form errors, JSON error responses for API

### Bonus (implemented)

- ✅ **Activity / history** — every status change and edit is logged per lead
- ✅ **Sorting** — sort leads by name, created date, status
- ✅ **Dashboard statistics** — counts per status, recent activity, conversion rate
- ✅ **Tests** — model, view, and API tests
- ✅ **API documentation** — see [`docs/API.md`](docs/API.md)
- ✅ **Docker** — `Dockerfile` + `docker-compose.yml` for local dev

---

## 🧱 Tech Stack

| Layer         | Technology                               |
| ------------- | ---------------------------------------- |
| Backend       | Django 5.x (pure Django, no DRF)         |
| Database      | PostgreSQL (SQLite fallback)             |
| Frontend      | Django Templates + Tailwind CSS          |
| UI Components | DaisyUI                                  |
| Auth          | Django session auth + Token auth for API |
| Container     | Docker + docker-compose                  |
| Testing       | Django `TestCase`                        |

---

## 🏗 Architecture

### Project layout

```
mini_crm/
├── config/                 # project settings, urls, wsgi
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   └── urls.py
├── apps/
│   ├── accounts/           # custom User, auth views, API token
│   ├── leads/              # Lead model, views, API, forms
│   │   ├── models.py
│   │   ├── managers.py
│   │   ├── forms.py
│   │   ├── views/
│   │   │   ├── web.py      # server-rendered pages
│   │   │   └── api.py      # JSON API
│   │   ├── selectors.py    # read queries (filtering, pagination)
│   │   ├── services.py     # write logic (create, update, status change)
│   │   └── tests/
│   └── activities/         # Activity log for leads
├── templates/              # base + app templates (Tailwind/DaisyUI)
├── static/                 # compiled CSS, JS
├── docs/
│   └── API.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

### Design decisions

1. **Pure Django over DRF.**
   The task explicitly says "pure Django". I implemented the API using Django's `JsonResponse`, class-based `View`s, and manual serialization. This keeps dependencies minimal and shows understanding of HTTP handling, validation, and pagination from first principles.

2. **Service + Selector pattern.**
   - `selectors.py` — all read queries (filtering, search, pagination) live here, keeping views thin.
   - `services.py` — all write operations (create lead, change status, log activity) are transactions with clear boundaries.
     This separation makes business logic testable without hitting views.

3. **Activity as a separate app.**
   The `activities` app stores immutable records (`actor`, `lead`, `action`, `from_status`, `to_status`, `timestamp`). It uses a generic FK so it can later track other entities.

4. **Status transitions are validated.**
   Allowed transitions are defined in `Lead.STATUS_TRANSITIONS`. Attempting an invalid transition (e.g. `Lost → New`) returns a 400 error. This is enforced at the service layer, not the view.

5. **Two auth mechanisms.**
   - **Session auth** for the web UI (login page, `@login_required`).
   - **Token auth** for the API (`Authorization: Token <key>`), implemented via a simple `ApiToken` model.

6. **API error envelope.**
   All API errors return a consistent shape:

   ```json
   {
     "error": {
       "code": "validation_error",
       "message": "...",
       "fields": { "name": ["..."] }
     }
   }
   ```

7. **Tailwind + DaisyUI via CDN for dev, compiled for prod.**
   Dev uses the Tailwind Play CDN for iteration speed; production runs a PostCSS build (see `package.json`).

---

## 🚀 Quick Start

### Option 1 — Local (SQLite)

```bash
# 1. Clone
git clone https://github.com/<your-username>/mini-crm.git
cd mini-crm

# 2. Virtualenv
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install deps
pip install -r requirements.txt

# 4. Env
cp .env.example .env
# edit .env if needed (defaults work with SQLite)

# 5. Migrate + seed
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_leads        # optional demo data

# 6. Run
python manage.py runserver
```

Visit:

- Web UI — http://localhost:8000/
- Admin — http://localhost:8000/admin/
- API — http://localhost:8000/api/v1/

### Option 2 — Docker (Postgres)

```bash
cp .env.example .env
docker compose up --build

# in another terminal:
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

App runs on http://localhost:8000.

---

## 🔌 API Reference (summary)

Base URL: `/api/v1/`

| Method | Endpoint                  | Description                                 | Auth   |
| ------ | ------------------------- | ------------------------------------------- | ------ |
| POST   | `/auth/login/`            | Obtain API token                            | Public |
| POST   | `/auth/logout/`           | Revoke token                                | Token  |
| GET    | `/leads/`                 | List leads (paginate, filter, search, sort) | Token  |
| POST   | `/leads/`                 | Create lead                                 | Token  |
| GET    | `/leads/{id}/`            | Retrieve lead                               | Token  |
| PATCH  | `/leads/{id}/`            | Partial update                              | Token  |
| DELETE | `/leads/{id}/`            | Delete lead                                 | Token  |
| POST   | `/leads/{id}/status/`     | Change status (validated transition)        | Token  |
| GET    | `/leads/{id}/activities/` | Activity log for a lead                     | Token  |
| GET    | `/stats/`                 | Dashboard statistics                        | Token  |

**Query params for `GET /leads/`:**

- `?status=New` — filter by status
- `?search=ali` — search name/phone/email
- `?ordering=-created_at` — sort (`name`, `created_at`, `status`)
- `?page=2&page_size=20` — pagination

Full request/response examples: [`docs/API.md`](docs/API.md).

---

## 🧪 Testing

```bash
python manage.py test
# or
pytest
```

Coverage includes:

- Model validation (phone/email rules, status transitions)
- Service layer (create, update, status change + activity logging)
- API endpoints (auth required, pagination, filtering, error shapes)
- Web views (login required, list filters, detail edit)

---

## 🗃 Data Model (simplified)

```
User
 └─ id, email, password, name

Lead
 ├─ id
 ├─ name
 ├─ phone (nullable, unique w/ email constraint)
 ├─ email (nullable)
 ├─ source (enum: website, referral, call, ads, other)
 ├─ note (text)
 ├─ status (enum: New | Contacted | Qualified | Won | Lost)
 ├─ created_by → User
 ├─ created_at, updated_at

Activity
 ├─ id
 ├─ lead → Lead
 ├─ actor → User
 ├─ action (created | updated | status_changed | note_added)
 ├─ from_status, to_status
 └─ created_at
```

**Constraint:** at least one of `phone` / `email` must be present (enforced in `Lead.clean()` and DB check constraint).

---

## 🤖 How I Used AI

Honest disclosure, per the task's requirement:

- **Scaffolding** — used AI to generate initial boilerplate (project layout, `requirements.txt`, Dockerfile). I reviewed and rewrote parts (e.g. switched from DRF to pure Django API, restructured into service/selector pattern).
- **Templates** — AI drafted some DaisyUI component markup. I verified the classes, adjusted spacing, and replaced generic components with ones fitting the data.
- **Tests** — AI suggested test cases; I wrote the assertions and edge cases myself (invalid status transitions, missing phone+email, unauthorized API access).
- **What I did NOT outsource** — the data model, status-transition rules, service layer logic, API design (error envelope, pagination format), and architecture decisions. These reflect my own reasoning and are explained above.
- **Verification** — every AI-generated snippet was read line-by-line, tested, and adjusted. Anything I couldn't explain, I removed.

---

## 📁 Environment Variables

| Variable               | Default                | Notes                  |
| ---------------------- | ---------------------- | ---------------------- |
| `DJANGO_SECRET_KEY`    | dev-insecure-key       | Change in prod         |
| `DJANGO_DEBUG`         | `True`                 | Set `False` in prod    |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1`  | Comma-separated        |
| `DATABASE_URL`         | `sqlite:///db.sqlite3` | Postgres URL supported |

---

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 👤 Author

**Alisher**

- GitHub: [@flat](https://github.com/flat07/lead_management)
