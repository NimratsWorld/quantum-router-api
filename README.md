# Quantum API Factory

A production-ready, modular Monolith architecture built with FastAPI.

## Features
- **RBF Router**: An AI-based routing module that classifies queries to save compute costs.
- **Data Insights**: Extracts structural entities (URLs, Emails) and analyzes text metrics.
- **Orchestrator**: Demonstrates API-to-API orchestration with graceful degradation (timeouts).
- **Zero-Trust Security**: Requires `X-API-Key` and uses IP-based Rate Limiting (`slowapi`).

## Quick Start
1. `pip install -r requirements.txt`
2. `uvicorn app.main:app --reload`
3. Open `http://127.0.0.1:8000/docs`

**API Key for Swagger:** `quantum-factory-secret-2026`