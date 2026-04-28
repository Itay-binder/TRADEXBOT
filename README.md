# TRADEXBOT

Infrastructure for an automated trading assistant that:

- scans markets continuously on configurable timeframes (5m / 15m and more),
- monitors economic news calendars for market-moving events,
- produces strategy-based AI trading signals,
- routes signals to WhatsApp and execution platforms (for example PickMyTrade),
- provides a management dashboard for configuration and monitoring.

## Disclaimer

This project is a technical foundation and **not financial advice**.  
Always paper-trade and validate risk controls before connecting to live accounts.

## Architecture

- `backend/` - FastAPI service, signal engine, connectors, API.
- `dashboard/` - Streamlit admin/monitoring interface (legacy local control panel).
- `frontend/` - Next.js web dashboard (recommended UI for Vercel).
- `.github/workflows/` - CI and deployment automation.
- `docker-compose.yml` - local orchestration.
- `render.yaml` - Render blueprint for backend web service and scanner worker.

## Features in this scaffold

- Configurable timeframes and strategy selection via API.
- Pluggable connector interfaces for:
  - TradingView market data feed,
  - economic calendar providers,
  - trade execution (PickMyTrade style),
  - notifications (WhatsApp webhook).
- Signal orchestration pipeline with:
  - indicator calculation placeholder,
  - AI model inference placeholder,
  - risk metadata in signal output.
- Dashboard for:
  - runtime status,
  - active configuration visibility,
  - API-based health check.
- CI workflow (pytest + Ruff).
- CD workflow template for container deployment.

## Quick start

### 1) Configure environment

Copy `.env.example` to `.env` and update keys:

- `TRADINGVIEW_API_KEY`
- `ECONOMIC_CALENDAR_API_KEY`
- `WHATSAPP_WEBHOOK_URL`
- `PICKMYTRADE_API_KEY`

### 2) Run with Docker

```bash
docker compose up --build
```

Backend: `http://localhost:8000`  
Dashboard: `http://localhost:8501`

### 3) Run backend locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

### 4) Run Next.js frontend locally

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Frontend: `http://localhost:3000`

## API outline

- `GET /health` - service health.
- `GET /config` - current runtime configuration.
- `POST /config` - update timeframe/strategy/connectivity settings.
- `POST /scan` - run one market scan cycle and return generated signals.

## Production next steps

- Add real provider clients:
  - TradingView webhook or broker feed bridge,
  - economic calendar provider (e.g. Investing / ForexFactory-compatible source),
  - WhatsApp Business API provider.
- Replace `AIModelStub` with trained model service.
- Add persistence (PostgreSQL + Redis + job queue).
- Add authentication (JWT + role-based access).
- Add broker-specific trade guardrails and max risk per trade.

## Deployment plan (recommended)

- Backend + Worker: Render using `render.yaml` (EU region set to Frankfurt).
- Frontend: Vercel (`frontend/`) with `NEXT_PUBLIC_BACKEND_URL` set to Render backend URL.
- Keep trading mode in paper until you validate signal quality and automation safety.
