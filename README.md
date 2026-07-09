# AI-Powered Password Strength Checker

[![Repository](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/oladotun1105/password-strength-checker)

> **Repository:** [https://github.com/oladotun1105/password-strength-checker](https://github.com/oladotun1105/password-strength-checker)

A full-stack, AI-powered password strength checker that combines client-side machine learning inference (XGBoost via ONNX Runtime), pattern analysis (zxcvbn), data breach detection (HIBP), and LLM-driven personalized advice streaming (Groq / Llama 3.3) — all without ever sending the raw password to a server.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
  - [Health Check](#health-check)
  - [POST /api/analyse](#post-apianalyse)
  - [POST /api/advise](#post-apiadvise)
- [Frontend Architecture](#frontend-architecture)
  - [Pages](#pages)
  - [Components](#components)
  - [Composables](#composables)
- [ML Pipeline](#ml-pipeline)
  - [Feature Vector](#feature-vector)
  - [Training](#training)
  - [Export to ONNX](#export-to-onnx)
  - [Client-Side Inference](#client-side-inference)
- [Data Flow](#data-flow)
- [Policy Rules Engine](#policy-rules-engine)
- [Security Model](#security-model)
- [Deployment Considerations](#deployment-considerations)
- [License](#license)

---

## Features

- **Client-side ML inference** — An XGBoost model exported to ONNX runs directly in the browser via ONNX Runtime Web (WASM), producing a 0–100 strength score with zero server round-trips.
- **Pattern detection** — zxcvbn runs client-side to detect dictionary words, keyboard walks, l33t substitutions, date patterns, repeated characters, and sequential patterns.
- **Data breach lookup** — Passwords are SHA-1 hashed on the client, and only a 5-character prefix is sent to the backend, which performs a k-anonymity range lookup against the Have I Been Pwned (HIBP) API.
- **AI-powered advice** — Analysis metadata (never the password itself) is sent to the backend, which streams personalized, jargon-free security advice via Groq's Llama 3.3 70B model using Server-Sent Events (SSE).
- **Policy rules checklist** — 11 configurable password policy rules are evaluated client-side and displayed as an interactive checklist.
- **Premium UI** — Dark glassmorphism design with Outfit + Plus Jakarta Sans typography, gradient strength bars, ambient glow effects, and smooth micro-animations.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐ │
│  │  zxcvbn  │  │  Policy  │  │  ONNX Runtime (WASM)   │ │
│  │ (pattern │  │  Rules   │  │  XGBoost model → 0-100 │ │
│  │ analysis)│  │  Engine  │  │  strength score        │ │
│  └────┬─────┘  └────┬─────┘  └───────────┬────────────┘ │
│       │              │                    │              │
│       └──────────────┴────────────────────┘              │
│                      │                                   │
│            SHA-1 hash (prefix only)                      │
│            + analysis metadata                           │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼───────────────────────────────────┐
│                  FastAPI Backend                          │
│                                                          │
│  ┌──────────────────┐     ┌─────────────────────────┐    │
│  │  /api/analyse    │     │  /api/advise            │    │
│  │  HIBP k-anon     │     │  Groq Llama 3.3 70B    │    │
│  │  breach lookup   │     │  SSE streaming advice   │    │
│  └──────────────────┘     └─────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
password-strength-checker/
├── frontend/                          # Nuxt 3 application
│   ├── app.vue                        # Root component with SEO head tags
│   ├── assets/css/main.css            # Global styles, CSS variables, design tokens
│   ├── components/
│   │   ├── advice-card.vue            # Streaming AI advice display
│   │   ├── breach-banner.vue          # Data breach warning banner
│   │   ├── password-input.vue         # Password text input with toggle
│   │   ├── rule-checklist.vue         # Policy rules checklist
│   │   ├── stats-row.vue              # ML score, crack time, zxcvbn stats
│   │   └── strength-bar.vue           # Animated gradient strength bar
│   ├── composables/
│   │   ├── use-advise.ts              # SSE streaming advice mutation
│   │   ├── use-analyse.ts             # HIBP breach check mutation
│   │   ├── use-feature-extractor.ts   # 16-feature vector extraction
│   │   ├── use-model-inference.ts     # ONNX session management & inference
│   │   ├── use-policy-rules.ts        # 11-rule password policy engine
│   │   └── use-zxcvbn.ts              # zxcvbn wrapper with typed output
│   ├── pages/
│   │   └── index.vue                  # Main page (orchestrates all composables)
│   ├── plugins/                       # Nuxt plugins
│   ├── public/
│   │   ├── model/password-model.onnx  # Pre-trained XGBoost model (ONNX)
│   │   └── ort/                       # ONNX Runtime WASM binaries (auto-copied)
│   ├── scripts/
│   │   └── copy-ort-wasm.mjs          # Postinstall: copies ORT WASM to public/
│   ├── nuxt.config.ts                 # Nuxt configuration
│   └── package.json                   # Frontend dependencies
│
├── backend/                           # FastAPI application
│   ├── app/
│   │   ├── main.py                    # App entrypoint, CORS, router registration
│   │   ├── models/
│   │   │   └── schemas.py             # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   ├── analyse.py             # POST /api/analyse (HIBP breach check)
│   │   │   └── advise.py              # POST /api/advise  (LLM advice stream)
│   │   └── services/
│   │       ├── feature_extractor.py   # Re-export of ml/features.py
│   │       ├── hibp.py                # HIBP k-anonymity range lookup
│   │       └── llm.py                 # Groq Llama 3.3 streaming + prompt builder
│   ├── ml/
│   │   ├── features.py                # 16-feature extraction (mirrors frontend)
│   │   ├── train.py                   # XGBoost training with 5-fold CV
│   │   ├── export.py                  # XGBoost → ONNX export
│   │   └── requirements.txt           # ML-specific dependencies
│   ├── data/
│   │   ├── generate-dataset.py        # RockYou → passwords.csv generator
│   │   └── hash-passwords.py          # Password hashing utility
│   ├── sanity-check.py                # Quick ONNX model verification script
│   ├── requirements.txt               # Runtime dependencies
│   └── .env.example                   # Environment variable template
│
├── .python-version                    # Python 3.12
├── .gitignore
├── tsconfig.json
└── README.md
```

---

## Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| [Nuxt 3](https://nuxt.com) | Vue 3 meta-framework with SSR/SSG support |
| [TailwindCSS](https://tailwindcss.com) | Utility-first CSS framework |
| [ONNX Runtime Web](https://onnxruntime.ai) | Client-side ML inference via WebAssembly |
| [zxcvbn](https://github.com/dropbox/zxcvbn) | Password pattern analysis (Dropbox) |
| [TanStack Vue Query](https://tanstack.com/query) | Async state management for mutations |
| [TypeScript](https://typescriptlang.org) | Type-safe development with strict mode |

### Backend

| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com) | Async Python API framework |
| [Groq](https://groq.com) | Ultra-fast LLM inference (Llama 3.3 70B) |
| [httpx](https://www.python-httpx.org) | Async HTTP client for HIBP API calls |
| [Pydantic v2](https://docs.pydantic.dev) | Request/response validation with strict mode |
| [uvicorn](https://www.uvicorn.org) | ASGI server |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable loading |

### ML Pipeline

| Technology | Purpose |
|---|---|
| [XGBoost](https://xgboost.readthedocs.io) | Gradient boosted tree regression model |
| [scikit-learn](https://scikit-learn.org) | K-Fold cross-validation, metrics |
| [onnxmltools](https://github.com/onnx/onnxmltools) | XGBoost → ONNX format conversion |
| [pandas](https://pandas.pydata.org) | Dataset loading and preprocessing |

---

## Prerequisites

- **Python** ≥ 3.12 (see `.python-version`)
- **Node.js** ≥ 18
- **pnpm** (preferred) or npm
- A **Groq API key** ([console.groq.com](https://console.groq.com))

---

## Getting Started

### Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start the development server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Verify with:

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

### Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies (also runs postinstall to copy ORT WASM binaries)
pnpm install

# Start the development server
pnpm dev
```

The app will be available at `http://localhost:3000`.

> **Note:** The `postinstall` script automatically copies ONNX Runtime WebAssembly binaries from `node_modules/onnxruntime-web/dist` to `public/ort/`. This is required for client-side inference to work.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ | — | API key for Groq LLM inference |
| `ALLOWED_ORIGINS` | ❌ | `http://localhost:3000` | Comma-separated list of allowed CORS origins |

### Frontend (`nuxt.config.ts`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `NUXT_PUBLIC_BACKEND_BASE_URL` | ❌ | `http://localhost:8000` | Backend API base URL |

---

## API Reference

### Health Check

```
GET /health
```

**Response** `200 OK`

```json
{
  "status": "ok"
}
```

---

### POST /api/analyse

Performs a **HIBP k-anonymity breach check** using a SHA-1 hash prefix/suffix pair. The backend never sees the raw password.

**Request Body**

```json
{
  "hashPrefix": "5BAA6",              // First 5 chars of SHA-1 hash (uppercase hex)
  "hashSuffix": "1E4C9B93F3F0682250B6CF8331B7EE68FD8"  // Remaining 35 chars
}
```

| Field | Type | Constraints |
|---|---|---|
| `hashPrefix` | `string` | Exactly 5 characters, pattern: `^[A-F0-9]{5}$` |
| `hashSuffix` | `string` | Exactly 35 characters, pattern: `^[A-F0-9]{35}$` |

**Response** `200 OK`

```json
{
  "isBreached": true,
  "breachCount": 9545824
}
```

| Field | Type | Description |
|---|---|---|
| `isBreached` | `boolean` | Whether the password hash was found in breach databases |
| `breachCount` | `integer` | Number of times the password appeared in breaches |

**Error Responses**

| Status | Description |
|---|---|
| `422` | Validation error (invalid hash format) |
| `502` | HIBP API lookup failed |

---

### POST /api/advise

Streams **personalized, AI-generated security advice** as Server-Sent Events (SSE). Accepts password analysis metadata — never the password itself.

**Request Body**

```json
{
  "strengthScore": 35,
  "zxcvbnScore": 1,
  "crackTime": "3 hours",
  "warning": "This is a commonly used password",
  "suggestions": ["Add more words that are less common"],
  "hasDictionaryMatch": true,
  "hasL33tSub": false,
  "hasKeyboardPattern": false,
  "hasDatePattern": false,
  "hasRepeat": false,
  "hasSequence": false,
  "rulesPassed": 4,
  "rulesTotal": 11,
  "isBreached": true,
  "breachCount": 9545824
}
```

| Field | Type | Description |
|---|---|---|
| `strengthScore` | `integer` | ML model score (0–100) |
| `zxcvbnScore` | `integer` | zxcvbn score (0–4) |
| `crackTime` | `string` | Human-readable estimated crack time |
| `warning` | `string` | zxcvbn warning message |
| `suggestions` | `string[]` | zxcvbn improvement suggestions |
| `hasDictionaryMatch` | `boolean` | Contains dictionary words |
| `hasL33tSub` | `boolean` | Contains l33t substitutions |
| `hasKeyboardPattern` | `boolean` | Contains keyboard walk patterns |
| `hasDatePattern` | `boolean` | Contains date patterns |
| `hasRepeat` | `boolean` | Contains repeated character blocks |
| `hasSequence` | `boolean` | Contains sequential patterns |
| `rulesPassed` | `integer` | Number of policy rules passed |
| `rulesTotal` | `integer` | Total number of policy rules |
| `isBreached` | `boolean` | Found in known data breaches |
| `breachCount` | `integer` | Number of breach occurrences |

**Response** — `text/event-stream`

```
data: Your password
data: has some
data: serious weaknesses...
data: [DONE]
```

The stream terminates with `data: [DONE]`.

**LLM Configuration**

| Parameter | Value |
|---|---|
| Model | `llama-3.3-70b-versatile` |
| Max Tokens | `600` |
| Provider | Groq |

---

## Frontend Architecture

### Pages

| File | Route | Description |
|---|---|---|
| `pages/index.vue` | `/` | Main page — orchestrates all composables, handles user input, manages reactive state, and coordinates the analysis → advice pipeline |

### Components

| Component | Props | Description |
|---|---|---|
| `password-input.vue` | `v-model` | Password text input with show/hide toggle |
| `strength-bar.vue` | `score: number` | Animated gradient progress bar with 5-tier labeling (Very Weak → Very Strong) |
| `stats-row.vue` | `mlScore`, `crackTime`, `zxcvbnScore` | Three-stat summary cards |
| `breach-banner.vue` | `isBreached`, `breachCount` | Conditional warning banner for breached passwords |
| `advice-card.vue` | `adviceText`, `isStreaming` | Streaming AI advice display with loading state |
| `rule-checklist.vue` | `rules: RuleResult[]` | Interactive policy rules checklist with pass/fail indicators |

### Composables

| Composable | Returns | Description |
|---|---|---|
| `useZxcvbn(password)` | `ZxcvbnResult` | Wraps the zxcvbn library with typed output including pattern flags |
| `useModelInference()` | `{ loadModel, predictStrength, isLoading, error }` | Manages ONNX session lifecycle and runs inference on a 16-feature vector |
| `usePolicyRules(password, zxcvbn)` | `PolicyResult` | Evaluates 11 password policy rules and returns pass/fail results |
| `extractFeatures(password, zxcvbn)` | `number[]` | Builds the 16-element feature vector for the ML model |
| `useAnalyse()` | TanStack `UseMutationReturn` | Mutation for the `/api/analyse` HIBP endpoint |
| `useAdvise()` | `{ adviceText, isStreaming, startAdvise }` | SSE streaming mutation for the `/api/advise` endpoint |

---

## ML Pipeline

### Feature Vector

Both the frontend (TypeScript) and backend (Python) extract an identical 16-dimensional feature vector from a password:

| Index | Feature | Type | Description |
|---|---|---|---|
| 0 | `length` | `float` | Character count |
| 1 | `entropyBits` | `float` | Shannon entropy (bits per character) |
| 2 | `hasUppercase` | `0 \| 1` | Contains uppercase letters |
| 3 | `hasLowercase` | `0 \| 1` | Contains lowercase letters |
| 4 | `hasDigits` | `0 \| 1` | Contains numeric digits |
| 5 | `hasSpecialChars` | `0 \| 1` | Contains non-alphanumeric characters |
| 6 | `uniqueCharRatio` | `float` | Unique characters / total length |
| 7 | `charClassCount` | `float` | Sum of character class flags (0–4) |
| 8 | `zxcvbnScore` | `float` | zxcvbn score (0–4) |
| 9 | `zxcvbnGuessesLog10` | `float` | log₁₀ of estimated guesses |
| 10 | `hasDictionaryMatch` | `0 \| 1` | Contains dictionary word matches |
| 11 | `hasL33tSub` | `0 \| 1` | Contains l33t substitutions |
| 12 | `hasKeyboardPattern` | `0 \| 1` | Contains spatial keyboard patterns |
| 13 | `hasDatePattern` | `0 \| 1` | Contains date patterns |
| 14 | `hasRepeat` | `0 \| 1` | Contains repeated character blocks |
| 15 | `hasSequence` | `0 \| 1` | Contains sequential patterns (abc, 123) |

### Training

The model is trained using XGBoost regression with 5-fold cross-validation:

```bash
cd backend

# Install ML dependencies
pip install -r ml/requirements.txt

# Generate training dataset from a password list (e.g., RockYou)
# Place your password list as data/RockYou.txt
python data/generate-dataset.py

# Train the model (outputs ml/password-model.xgb)
python ml/train.py

# Optional: limit dataset size for faster iteration
python ml/train.py --max-rows 100000
```

**Training configuration:**

| Parameter | Value |
|---|---|
| Algorithm | XGBRegressor |
| Estimators | 300 |
| Max Depth | 6 |
| Learning Rate | 0.1 |
| Subsample | 0.8 |
| Col Sample by Tree | 0.8 |
| Cross-Validation | 5-fold KFold |

**Label scaling:** `guesses_log10` values are scaled to a 0–100 range using the formula:

```
score = clip((guesses_log10 / 18.0) × 100, 0, 100)
```

### Export to ONNX

```bash
cd backend
python ml/export.py
# → Saves ONNX model to frontend/public/model/password-model.onnx
```

The export script converts the trained XGBoost model (`.xgb`) to ONNX format with a `FloatTensorType([None, 16])` input shape, making it compatible with ONNX Runtime Web.

### Client-Side Inference

The `useModelInference` composable manages the full ONNX lifecycle:

1. **Session caching** — The ONNX `InferenceSession` is created once and shared across all composable instances via a module-level promise.
2. **Pre-warming** — `loadModel()` is called in `onMounted()` so the model is ready before the user types.
3. **Inference** — `predictStrength(features)` validates the 16-element input, runs the ONNX session, and clamps the output to 0–100.
4. **WASM paths** — The ORT WASM binaries are served from `/ort/` (copied at install time by `scripts/copy-ort-wasm.mjs`).

---

## Data Flow

```
User types password
        │
        ├──► useZxcvbn(password)
        │         │
        │         ├──► Pattern flags (dictionary, l33t, spatial, ...)
        │         ├──► Crack time estimate
        │         └──► Score (0–4), guesses_log10
        │
        ├──► extractFeatures(password, zxcvbnResult)
        │         │
        │         └──► 16-element float vector
        │                   │
        │                   └──► useModelInference.predictStrength(vector)
        │                              │
        │                              └──► Strength score (0–100)
        │
        ├──► usePolicyRules(password, zxcvbnResult)
        │         │
        │         └──► 11 rule results + passed/total counts
        │
        ├──► SHA-1(password) → prefix (5 chars) + suffix (35 chars)
        │         │
        │         └──► POST /api/analyse { hashPrefix, hashSuffix }
        │                   │
        │                   └──► HIBP k-anonymity lookup
        │                              │
        │                              └──► { isBreached, breachCount }
        │
        └──► User clicks "Get personalized advice"
                  │
                  └──► POST /api/advise { analysis metadata, no password }
                            │
                            └──► Groq Llama 3.3 70B streaming (SSE)
                                       │
                                       └──► Real-time advice text
```

---

## Policy Rules Engine

The frontend evaluates **11 password policy rules** client-side:

| # | Rule | Condition |
|---|---|---|
| 1 | Minimum length | `length ≥ 8` |
| 2 | Strong length | `length ≥ 12` |
| 3 | Uppercase letters | Contains `[A-Z]` |
| 4 | Lowercase letters | Contains `[a-z]` |
| 5 | Digits | Contains `[0-9]` |
| 6 | Special characters | Contains `[!@#$%^&*()_+\-=[\]{}|;:,.<>?]` |
| 7 | No sequential patterns | No zxcvbn `sequence` pattern detected |
| 8 | No repeated characters | No zxcvbn `repeat` pattern detected |
| 9 | No dictionary words | No zxcvbn `dictionary` pattern detected |
| 10 | No keyboard patterns | No zxcvbn `spatial` pattern detected |
| 11 | Not a common password | zxcvbn `score ≠ 0` |

---

## Security Model

| Concern | Mitigation |
|---|---|
| **Password exposure** | Raw passwords never leave the browser. All analysis (zxcvbn, ML inference, policy rules) runs client-side. |
| **Breach check privacy** | Uses HIBP's k-anonymity model: only a 5-character SHA-1 prefix is sent to the API. The backend matches the suffix locally from the response. |
| **LLM data leakage** | Only analysis metadata (scores, flags, crack time) is sent to the `/api/advise` endpoint. The password itself is never included. |
| **API key security** | The `GROQ_API_KEY` is loaded from `.env` and never exposed to the frontend. |
| **CORS** | Origins are restricted via the `ALLOWED_ORIGINS` environment variable (defaults to `http://localhost:3000`). |
| **Input validation** | Pydantic strict mode validates all request bodies. Hash fields enforce exact length and hex-character patterns. |
| **HIBP User-Agent** | A fixed `password-strength-checker/1.0` User-Agent is sent with all HIBP requests per API guidelines. |

---

## Deployment Considerations

### Frontend (Nuxt 3)

- Deploy as a static site (`nuxt generate`) or server-rendered app.
- Set `NUXT_PUBLIC_BACKEND_BASE_URL` to the production backend URL.
- Ensure the `public/model/password-model.onnx` and `public/ort/` WASM binaries are included in the build.

### Backend (FastAPI)

- Runtime dependencies are intentionally minimal for platforms like Vercel and Railway.
- Set `GROQ_API_KEY` and `ALLOWED_ORIGINS` as environment variables in your hosting platform.
- The backend is stateless and can be horizontally scaled.

### ML Retraining

- Place a password list (e.g., RockYou) at `backend/data/RockYou.txt`.
- Run `generate-dataset.py` → `train.py` → `export.py`.
- Commit the updated `frontend/public/model/password-model.onnx` to the repository.

---

## License

This project is open source. See the repository for license details.
