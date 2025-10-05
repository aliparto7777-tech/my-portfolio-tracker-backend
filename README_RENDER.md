My Portfolio Tracker - FastAPI backend (Render-ready, SQLite, clean)
------------------------------------------------------------------

This repository is prepared for a one-click deploy to Render (Docker). The database starts empty; you will register a user after deployment.

Quick steps to deploy on Render:
1. Create a GitHub repository and push this project to it.
2. Sign in at https://render.com and click 'New' -> 'Web Service'.
3. Connect your GitHub repo, select the branch, and choose Docker.
4. Use the default start command (uvicorn app.main:app --host 0.0.0.0 --port $PORT).
5. After deploy completes, open https://<your-service>.onrender.com/docs to access the API docs.
6. Copy `.env.example` to `.env` on your local dev if you run locally; set a strong SECRET_KEY.

Local run (for testing):
- Create virtualenv, install requirements, and run:
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload

Endpoints of interest:
- POST /auth/register  (body: {email, password})
- POST /auth/login     (form data: username=email, password)
- /accounts and /transactions endpoints protected by Bearer token
- /sync/push and /sync/pull for client sync

Notes:
- This build uses SQLite for simplicity. For production with multiple users, consider PostgreSQL and update DATABASE_URL accordingly.
