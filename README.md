# Campaign Hub

**INF601 - Advanced Programming in Python | Mini Project 6 | Gage Giffin**

Campaign Hub is a Django web app for running Dungeons & Dragons campaigns. Any registered user can create a campaign and become its Dungeon Master (DM). Other users join with an invite code and become players. Each campaign keeps a session log of recaps and a directory of NPCs (non-player characters). The DM can keep secret notes and hidden NPCs that players never see.

## Features

- **Accounts:** register, log in and log out using Django's built-in authentication.
- **Campaigns:** create, edit and delete campaigns. Each campaign gets a random invite code that players use to join.
- **Session Log:** the DM records each session's number, title, date played and recap, plus private DM notes.
- **NPC Directory:** NPCs with race, role and status (Alive / Dead / Unknown), filterable by status. Clicking an NPC opens a detail card in a modal.
- **DM secrets:** session DM notes, NPC secret notes and hidden NPCs are only visible to the campaign's DM.
- **Bootstrap 5 interface:** responsive layout with modals for joining a campaign, viewing NPC details and confirming deletes.
- **Customized Django admin:** campaign, session and NPC management with search, filters, inline editing and a collapsible "DM Secrets" section.

## Roles and Permissions

Permissions are enforced in the views and database queries, not just hidden in templates.

| Role | Can see | Can change |
|---|---|---|
| **DM** (campaign creator) | Everything, including secret notes and hidden NPCs | Create, edit and delete the campaign, its sessions and NPCs |
| **Player** (joined by invite code) | Campaign, sessions and visible NPCs, but no secrets | Nothing (read-only) |
| **Non-member** | Nothing: all campaign URLs return 404 | Nothing |

## Project Structure

```text
miniproject6GageGiffin/
├── manage.py
├── requirements.txt
├── .env.example          # template for the private .env settings file
├── mysite/               # project settings and root URLs
│   ├── settings.py       # reads secrets from .env
│   └── urls.py
├── accounts/             # registration and login/logout
│   ├── forms.py          # RegisterForm, LoginForm, BootstrapFormMixin
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/register.html
├── campaigns/            # main app
│   ├── models.py         # Campaign, GameSession, NPC
│   ├── admin.py          # ModelAdmin customization
│   ├── forms.py          # CampaignForm, JoinCampaignForm, GameSessionForm, NPCForm
│   ├── views.py          # all campaign/session/NPC views and permission helpers
│   ├── urls.py
│   ├── migrations/
│   └── templates/campaigns/
└── templates/            # project-wide templates
    ├── base.html         # Bootstrap layout every page extends
    ├── partials/         # shared form fields and delete modal
    └── registration/login.html
```

## Pages

| Page | URL | Access |
|---|---|---|
| Home | `/` | Everyone |
| Register | `/accounts/register/` | Everyone |
| Login | `/accounts/login/` | Everyone |
| My Campaigns | `/campaigns/` | Logged in |
| New / Edit Campaign | `/campaigns/new/`, `/campaigns/<id>/edit/` | Logged in / DM |
| Campaign Detail | `/campaigns/<id>/` | Members |
| Session Log | `/campaigns/<id>/sessions/` | Members |
| Session Detail | `/campaigns/<id>/sessions/<id>/` | Members |
| New / Edit Session | `/campaigns/<id>/sessions/new/`, `.../edit/` | DM |
| NPC Directory | `/campaigns/<id>/npcs/` | Members |
| New / Edit NPC | `/campaigns/<id>/npcs/new/`, `.../edit/` | DM |
| Admin | `/admin/` | Superuser |

## Requirements

- Python 3.13 (developed on 3.13.14)
- Git
- Python packages (in `requirements.txt`):
  - Django 6.1.2
  - python-dotenv 1.2.4
  - asgiref and sqlparse (Django dependencies)
- SQLite (built into Python; no separate database server needed)
- Internet access in the browser (Bootstrap is loaded from the jsDelivr CDN)

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/GagePi-Dev/miniproject6GageGiffin.git
cd miniproject6GageGiffin
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install the requirements

```bash
pip install -r requirements.txt
```

### 4. Create the .env settings file

Secrets are kept out of the repository in a `.env` file. Copy the template:

```bash
cp .env.example .env            # Linux / macOS
copy .env.example .env          # Windows
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then edit `.env`. For local development:

```text
DJANGO_SECRET_KEY=<paste the generated key>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

Never commit `.env`. It is already listed in `.gitignore`.

### 5. Initialize the database

```bash
python manage.py makemigrations
python manage.py migrate
```

The migration files are already in the repository, so `makemigrations` should report "No changes detected". `migrate` creates `db.sqlite3` with all the tables.

### 6. Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts for a username, optional email and password.

### 7. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser. The admin site is at http://127.0.0.1:8000/admin/.

## Using the App

1. **Register** an account. You are logged in automatically.
2. Go to **My Campaigns**, then **New Campaign**. You become its DM.
3. On the campaign page, copy the **invite code** (only the DM can see it).
4. Log in as a second user, open **My Campaigns**, then **Join Campaign** and enter the code.
5. As the DM, add sessions in the **Session Log** and characters in the **NPC Directory**. Mark an NPC as hidden, or add secret notes, and compare what the player account sees.

## Django Admin

Log in at `/admin/` with the superuser account.

- **Campaigns:** list with DM and player count, search by name or DM, a two-box player picker, and sessions and NPCs editable directly on the campaign page.
- **Game sessions:** filter by campaign, browse by date, and a collapsed "DM Secrets" section.
- **NPCs:** filter by campaign, status and hidden; status editable directly from the list; a collapsed "DM Secrets" section.

## AI Usage

This project was built with help from **Claude Code** (Anthropic's AI coding assistant), using the **Claude Opus 5.5** model at **Medium effort**, running in the terminal on the course dev box. I planned the project and made the design decisions. For each build step, Claude proposed a design, I approved or adjusted it, and then Claude wrote and tested the code. Every commit was made at my direction after I reviewed the step.

### What the AI Did

- **Planning and review:** reviewed my project plan, recommended answers to my open design decisions (two apps, invite codes, read-only players, function-based views, no stretch models for now) and wrote a design proposal before each build step.
- **Project cleanup:** created `.env.example`, staged the move of `requirements.txt` to the repo root, and added the INF601 header to generated files.
- **Models and admin (step 2):** created the `accounts` and `campaigns` apps, wrote the `Campaign`, `GameSession` and `NPC` models and the customized admin classes, and ran the migrations.
- **Templates and auth (step 3):** wrote `base.html` with Bootstrap 5, shared form templates, the register view and form, and set up Django's login/logout views.
- **Campaign pages (step 4):** wrote the list, detail, create, edit, delete and join views, the forms, and the join and delete modals.
- **Sessions and NPCs (step 5):** wrote the session log, session detail, NPC directory and forms, plus the NPC detail modal and status filter.
- **Security-focused testing:** wrote throwaway test scripts (rolled back, not part of the repo) checking that players can't see DM secrets or hidden NPCs, that non-members get 404s, that one DM can't reach another campaign's data by changing IDs in the URL, and that tampered form fields are ignored.
- **Troubleshooting:** found that a mismatched `CSRF_TRUSTED_ORIGINS` value was blocking logins on the public site (checked without displaying the `.env` values), restarted the dev server when needed, and ran Django's deployment checks.
- **Documentation:** drafted this README.

### What I Did Myself
- Set up the base Django web app by following the course instructions.
- Set up `settings.py` to read its settings from a `.env` file, so the project is safe to upload to GitHub.
- Came up with the Campaign Hub idea and planned the models, pages, forms, modals, admin setup, permissions and build order.
- Made the final call on each design decision and reviewed each step's proposal before it was built.
- Fixed the CSRF trusted origin in my `.env` file and created the superuser account.
- Decided when each step was committed.

### What I Changed In AI Code
- I made no manual edits to AI code. All edits were made through interacting with Claude Code.
