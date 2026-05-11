# AI-powered password strength checker

This monorepo contains:

- `frontend/`: Nuxt 3 app with local zxcvbn analysis, ONNX inference, policy checks, and streaming advice UI.
- `backend/`: FastAPI API for HIBP breach checks and Claude advice streaming.

## Project structure

```text
/
├── frontend/
└── backend/
```

## Development setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add your GROQ_API_KEY to .env
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
# runs on http://localhost:3000

# ML training (optional — a pre-trained model is not included)
cd backend
pip install -r ml/requirements.txt
python ml/train.py    # requires data/passwords.csv
python ml/export.py   # exports ONNX to frontend/public/model/
```

## Security notes

- Raw passwords are never sent to the backend.
- Backend secrets are loaded from `.env` (`GROQ_API_KEY`).
- CORS origins are controlled by `ALLOWED_ORIGINS`.
- HIBP uses k-anonymity style range lookup with a fixed User-Agent.
- Runtime backend dependencies are intentionally kept small for Vercel.
