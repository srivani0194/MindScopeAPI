# MindScope – Mood & Energy Tracker API

I built this app as part of a take-home challenge. I wanted it to be simple, clean, and something I’d actually enjoy using if I were logging how I feel every day. It’s basically a mood and activity tracker that’s fully backend-powered, with auth and rate limiting built-in.

If you’re reading this — thanks for reviewing!

---

## What It Does

* Users can register, log in, and get a secure JWT token
* You can track your mood, energy, and activity for any day
* Rate limiting: 20 requests per minute globally, 5 per minute on mood creation
* `/summary` route shows how your week’s been (Happy, Sad, etc.)
* Swagger UI at `/docs` makes it easy to explore and test everything

---

## Tech I Used

* FastAPI – fast, clean, and modern
* SQLite – lightweight and perfect for local builds
* SQLAlchemy – ORM to make database work easier
* JWT via `python-jose` – for secure authentication
* Rate limiting via `slowapi`
* Password hashing – using `passlib[bcrypt]`

---

## Auth and Rate Limiting

* All mood routes are JWT-protected
* Global limit: 20 requests per minute
* `POST /mood`: tighter limit of 5 per minute

---

## How to Run It

```bash
git clone https://github.com/your-username/mindscope.git
cd mindscope
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then go to: [http://localhost:8000/docs](http://localhost:8000/docs) and test away.

---

## Sample Weekly Summary

```json
{
  "summary": {
    "Happy": 3,
    "Tired": 2
  },
  "week_start": "2025-05-05",
  "today": "2025-05-07"
}
```

---

## Why This Stack?

* FastAPI helped me build and test quickly
* SQLite was just right for a local app
* JWT made auth secure but lightweight
* I added rate limiting because it's practical and often overlooked
* Swagger UI was super helpful for testing without needing a frontend

---

## Challenge Requirements – Covered

As per point (b): “Design and implement an API server with authentication and rate limiting”

* Auth with hashed passwords and JWT – done
* Rate limiting with `slowapi` – done
* A working API server with real endpoints and documentation – done

---
