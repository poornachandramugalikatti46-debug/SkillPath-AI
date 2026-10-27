# SkillPath AI

AI/ML-Based Student Career Readiness, Resume & Skill-Gap Analysis System

## Run locally

Start MongoDB, then run the backend from the repository root:

```powershell
python -m uvicorn backend.main:app --reload
```

In another terminal, start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

The backend runs at `http://127.0.0.1:8000` by default (or `--port 8001`). The frontend connects to `http://127.0.0.1:8000` by default (configurable via `VITE_API_URL` in `frontend/.env`) and includes an automatic fallback between port 8000 and 8001. Verify the backend is running at `http://127.0.0.1:8000/health` (or `8001/health`) before using login or registration.

## Google sign-in setup

Set `VITE_GOOGLE_CLIENT_ID` in `frontend/.env` and `GOOGLE_CLIENT_ID` in the
repository-root `.env` to the **same** Google OAuth web client ID. In that
client's Google Cloud Console settings, add the frontend origin as an authorized
JavaScript origin (for the default Vite server, add both
`http://localhost:5173` and `http://127.0.0.1:5173`). Restart the frontend
and backend after changing their environment files. Google sign-in will
otherwise fail with a 403 origin-not-allowed response or backend
credential-verification error.

## Project Goal

SkillPath AI analyzes a student's education, skills, resume,
GitHub activity, assessments, and career goals to generate
data-driven career readiness and skill-gap insights.

## Main ML Components

- Career Readiness Classification
- Readiness Score Regression
- Student Clustering
- Career Role Matching
- Resume NLP
- Skill Gap Analysis
- Project Recommendation
- Explainable AI using SHAP