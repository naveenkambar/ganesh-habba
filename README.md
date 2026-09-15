# Yuvaka Mandala — Ganeshotsav Website (Django Version)

Same site, same design, rebuilt on **Django** instead of Flask. Real
database (SQLite by default), runs on any hosting service, works in any
browser for anyone — nothing tied to Claude.

Default committee password: **ganpati123** — change it from inside the site
after you deploy (Committee Login → Change Password).

## ⚠️ Please test this locally first

I built this by mirroring the exact same API design as an earlier Flask
version I tested live and confirmed working (login, saving entries, unique
receipt numbers, deleting, and data surviving a page reload). I was **not**
able to run this exact Django version in a live server myself before
sending it to you — Django wasn't available in my testing environment this
time. The code has been checked for errors but not run end-to-end, so
please follow "Run it locally" below first and try the whole site (login,
add an entry, delete an entry, reload the page) before deploying it live.
If anything misbehaves, tell me exactly what happened and I'll fix it.

## What's inside
- `manage.py` — Django's command-line tool.
- `ganesh_project/` — project settings and URL routing.
- `festival/` — the app: database models (`models.py`) and the API (`views.py`).
- `templates/index.html` — the website itself (same design as before).
- `requirements.txt`, `Procfile` — for deployment.

## Run it locally (do this first)

1. Install Python 3 if you don't have it (https://python.org).
2. Open a terminal in this folder and run:
   ```
   pip install -r requirements.txt
   python manage.py makemigrations festival
   python manage.py migrate
   python manage.py runserver
   ```
3. Open `http://127.0.0.1:8000` in your browser.
4. Try: Committee Login (password `ganpati123`) → add a schedule item → add
   a collection entry → try a duplicate receipt number (should be rejected)
   → delete an entry → refresh the page (your data should still be there).

## Deploy for free on Render.com

1. Go to https://render.com and sign up (free, no credit card).
2. Put this folder in a GitHub repository.
3. In Render: **New +** → **Web Service** → connect your repo.
4. Render will use the `Procfile` automatically. Confirm:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python manage.py migrate --noinput && gunicorn ganesh_project.wsgi`
5. Click **Create Web Service**. Wait a couple of minutes for the first deploy.
6. You'll get a free public link like `https://yuvaka-mandala.onrender.com`
   — share it on WhatsApp.

## Deploy on PythonAnywhere (alternative, has native Django support)

1. Sign up free at https://www.pythonanywhere.com
2. Upload these files via their "Files" tab.
3. Go to "Web" tab → Add a new web app → choose **Django**.
4. Point it at this project (`ganesh_project`), run the migrate commands
   they show you in their console.
5. They give you a free link like `yourname.pythonanywhere.com`.

## Important notes
- `ganesh.db` (SQLite) is created automatically the first time you run
  `migrate`, and stores everything permanently.
- Receipt numbers for collections are enforced unique by the database
  itself — duplicates are rejected automatically with a clear message.
- Before deploying live for real public use, change `SECRET_KEY` in
  `ganesh_project/settings.py` to something random, and set `DEBUG = False`
  (via the `DJANGO_DEBUG=False` environment variable on your host).
- To back up your data, download `ganesh.db` from your hosting platform's
  file manager occasionally.
