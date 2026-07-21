# SocialPulse

A complete Django social media platform — feed, profiles, likes, comments, follows, friend requests, real-time notifications (WebSockets via Channels), DRF REST API, and a full **admin dashboard** with charts and CRUD.

Theme: **Neon Sunset** with three switchable looks (Light / Dusk / Dark).

## Stack
- Django 4.2+ · Channels · DRF · SimpleJWT
- Bootstrap 5.3 + Bootstrap Icons + Chart.js
- SQLite by default · WhiteNoise · Crispy Forms

## Quick Start
```bash
unzip socialpulse.zip
cd socialpulse
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations accounts posts social notifications
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:
- `/` — Home feed
- `/accounts/signup/` — Sign up
- `/dashboard/` — Admin dashboard (staff only)
- `/admin/` — Django admin
- `/api/v1/` — REST API root

## Real-time Notifications
Run with Daphne for WebSocket support:
```bash
daphne -p 8000 config.asgi:application
```

## Features
- Custom User with avatar, cover, bio, privacy & theme preference
- Posts with image/video, privacy levels, profanity auto-censor
- Likes, threaded comments, follow + friend requests
- WebSocket toasts for new notifications
- REST API with JWT auth (`/api/v1/auth/token/`)
- Theme switcher (Light · Dusk · Dark) — preference saved per user
- Admin dashboard:
  - KPI tiles, 14-day activity chart, privacy doughnut
  - User CRUD with active/staff toggles
  - Post moderation (flag, hide, delete)
  - Comment moderation
  - Broadcast announcement to all users

## Project layout
```
socialpulse/
├─ config/           # settings, urls, asgi
├─ accounts/         # custom User, profile, themes
├─ posts/            # posts, comments, likes
├─ social/           # follows, friend requests
├─ notifications/    # Channels consumers + REST
├─ api/              # DRF viewsets
├─ dashboard/        # admin dashboard (CBVs)
├─ templates/        # all HTML (Bootstrap 5.3)
└─ static/css|js     # external theme.css & app.js
```

## Deploy
Production: collectstatic, run with Daphne behind Nginx; switch DATABASES to Postgres and CHANNEL_LAYERS to Redis for multi-process workers.
