# Money OS — Personal Finance Operating System

Track, manage, and optimize your finances with a modern full-stack application.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS v4, ShadCN UI |
| **Backend** | FastAPI, SQLAlchemy (async), Python |
| **Database** | Neon PostgreSQL (serverless) |
| **Authentication** | Clerk |
| **Hosting** | Vercel (frontend) / Railway (backend) |

## Project Structure

```
money-os/
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/       # App Router pages & layouts
│   │   ├── components/# Reusable UI components
│   │   ├── lib/       # Utilities & helpers
│   │   ├── hooks/     # Custom React hooks
│   │   └── types/     # TypeScript type definitions
│   └── ...
│
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/       # API route handlers
│   │   ├── core/      # Config, database, auth
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   └── ...
│
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.12+
- Clerk account (free at [clerk.com](https://clerk.com))
- Neon PostgreSQL account (free at [neon.tech](https://neon.tech))

### Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env.local` file with your Clerk keys:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

Run the dev server:

```bash
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/moneyos?sslmode=require
CLERK_SECRET_KEY=sk_test_...
CLERK_PUBLISHABLE_KEY=pk_test_...
ALLOWED_ORIGINS=http://localhost:3000
```

Run the dev server:

```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/stats` | Dashboard statistics |
| GET/POST | `/api/v1/transactions` | List/Create transactions |
| GET/PUT/DELETE | `/api/v1/transactions/{id}` | Transaction CRUD |
| GET/POST | `/api/v1/accounts` | List/Create accounts |
| GET/PUT/DELETE | `/api/v1/accounts/{id}` | Account CRUD |
| GET/POST | `/api/v1/budgets` | List/Create budgets |
| GET/PUT/DELETE | `/api/v1/budgets/{id}` | Budget CRUD |
| GET | `/health` | Health check |

## License

MIT
