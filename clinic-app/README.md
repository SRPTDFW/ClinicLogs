# SRPT Daily Clinic Log

A small web app for logging hydrocollator temperature checks, chemical usage,
and daily tasks across all SRPT clinic locations. Each clinic signs in with a
shared passcode; an admin login lets you manage passcodes, set the safe
temperature range, and see records across every clinic.

This is a real, independent web application — nobody needs a Claude account
to use it, and the data lives in a database on your hosting provider, not on
anyone's laptop.

## What's in here
- `app.py` — the whole backend (Flask + a database)
- `templates/`, `static/` — the pages staff and admins see
- `requirements.txt`, `Procfile` — tells the host how to run it

## Recommended deploy: Render (free web service) + Neon (free Postgres)

Total cost: $0 to start. No credit card required for either at time of writing.
Takes about 10–15 minutes.

### 1. Create the database (Neon)
1. Go to https://neon.tech and sign up (free tier).
2. Create a new project — any name is fine.
3. On the project dashboard, copy the **connection string** (it looks like
   `postgresql://user:password@ep-xxxx.neon.tech/dbname?sslmode=require`).
   Keep this handy for step 3.

### 2. Push this code to GitHub
1. Create a new (private is fine) repository on https://github.com.
2. Upload this whole folder to it — either drag-and-drop the files on
   GitHub's web UI, or use `git push` if you're comfortable with git.

### 3. Deploy on Render
1. Go to https://render.com and sign up (free tier).
2. Click **New > Web Service**, connect your GitHub account, and pick the
   repository you just created.
3. Render should auto-detect Python. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
4. Under **Environment Variables**, add:
   - `DATABASE_URL` — paste the Neon connection string from step 1
   - `SECRET_KEY` — any long random string (see `.env.example` for how to generate one)
   - `ADMIN_PASSCODE` — the passcode you'll use to sign in as admin
   - `DEFAULT_CLINIC_PASSCODE` — the starting passcode all 9 clinics will share
     on first login (change each one individually afterward from the admin panel)
5. Click **Create Web Service**. Render will build and deploy — takes a
   couple of minutes. You'll get a URL like `https://srpt-clinic-log.onrender.com`.

### 4. First login
1. Open your new URL, sign in as **admin** using `ADMIN_PASSCODE`.
2. From the admin panel, reset each clinic's passcode to something specific
   to that clinic, and set your preferred safe temperature range.
3. Share each clinic's URL + passcode with that clinic's staff. They sign in
   at the same URL, selecting their clinic from the dropdown.

## Notes
- **Free-tier sleep:** Render's free web services "sleep" after inactivity
  and take ~30 seconds to wake up on the next visit. If that's a problem,
  Render's cheapest paid tier ($7/mo at time of writing) keeps it always-on.
- **Backups:** Neon's free tier retains your data, but it's worth exporting
  the CSV periodically (built into the admin panel and clinic view) as your
  own backup.
- **Changing passcodes:** always done from the admin panel — no redeploy needed.
- **Alternative hosts:** Railway, Fly.io, or a plain VPS all work the same
  way — install `requirements.txt`, set the same environment variables, and
  run `gunicorn app:app`.

## Running it locally (optional, for testing before you deploy)
```
pip install -r requirements.txt
export SECRET_KEY=test
export ADMIN_PASSCODE=admin123
export DEFAULT_CLINIC_PASSCODE=clinic123
python app.py
```
Then visit http://localhost:5000
