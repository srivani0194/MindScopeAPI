# MindScope – Mood & Energy Tracker API

Hi, I’m Srivani — I built this app as part of a take-home challenge. My goal was to create something simple but meaningful — the kind of app I’d actually use. MindScope lets users track how they’re feeling and what’s affecting their energy each day. It’s secure, lightweight, and easy to deploy anywhere.

---

##  What It Does

- Users can register, log in, and receive a secure JWT token
- Track mood, energy, and activity for any day
- Global rate limit: 20 requests per minute
- Route-level limit: 5 requests/minute for mood creation
- `/summary` endpoint shows a quick emotional snapshot of the week
- Swagger UI at `/docs` to test everything without external tools

---

##  Tech Stack

- **FastAPI** – fast, clean Python framework
- **SQLite** – simple and portable database
- **SQLAlchemy** – ORM for easy database modeling
- **JWT with python-jose** – for stateless, secure login
- **SlowAPI** – for applying clean and controlled rate limits
- **passlib (bcrypt)** – secure password hashing
- **Docker** – containerized for portability
- **Terraform** – infrastructure-as-code
- **AWS EC2** – deployed and running in the cloud

---

##  Auth & Rate Limiting

- All protected routes require JWT
- Global rate limit: `20 req/min`
- POST `/mood`: `5 req/min` to prevent abuse

---

##  Run Locally

```bash
git clone https://github.com/your-username/mindscope.git
cd mindscope
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Go to: [http://localhost:8000/docs] to try it out.

---

##  Docker

```bash
docker build -t srivaniraob/mindscope-api:latest .
docker run -d -p 8000:8000 srivaniraob/mindscope-api:latest
```

## Deployed on AWS with Terraform

It also has full infrastructure-as-code setup to deploy everything on AWS EC2:

- Provisions EC2 (Amazon Linux 2)
- Installs Docker automatically using `user_data`
- Pulls and runs your Docker container
- Opens port `8000` via a security group
- Attaches an Elastic IP for a stable public address

**To deploy:**

```bash
cd infra
terraform init
terraform apply
```

Access the app at:
```
http://http://52.36.231.28:8000/docs
```

---

##  Sample Weekly Summary Output

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

##  Why This Stack?

I wanted something that:
- Was fast to prototype but clean to maintain
- Required minimal setup for reviewers
- Reflected how I’d build an API in real life

So I went with FastAPI, SQLite, JWT, and containerized deployment with Terraform on AWS. It felt natural and practical.

---

##  Challenge Requirements – Covered

###  Point (a): Containerized web app deployed on cloud
- Dockerized and published to Docker Hub
- Deployed on AWS EC2 via Terraform (infra-as-code)

###  Point (b): Build an API server with auth + rate limiting
- JWT-based login, hashed passwords
- Global + endpoint-specific rate limits with `slowapi`
- Interactive Swagger docs at `/docs`
- Bonus: `/summary` route to visualize logged data over time

---


