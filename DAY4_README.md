# Day 4 — Deploy CrewAI as an API Service (2-hour live coding)

## 🎯 Title & Topic
Ship the Multi-Agent Book Generator as an API — FastAPI, Uvicorn, and Demo-Ready Operations

## Overview (long form)

This Day 4 module completes the 4-day journey by converting the existing CrewAI flow into a simple API service that students can call from Postman, curl, or another app. Instead of teaching deployment only as scripts/CLI, this lesson focuses on API-first operational delivery.

Students will learn how to expose the current flow through minimal HTTP endpoints, run it with FastAPI + Uvicorn, validate requests/responses, and deploy it in a simple, reproducible way.

The class keeps the same instructor-friendly structure as previous days: clear timeline, setup, walkthrough, live coding, troubleshooting, quiz, exercises, and handoff checklist.

By the end of Day 4, learners can run and present this project as a basic API service with a health endpoint and generation endpoint.

## **SESSION FLOW**

### **What We'll Cover Today (Step-by-Step)**

1. **Recap Days 1–3 and Day 4 outcomes** (10 min)
  - Review foundations, concurrency, and output quality improvements
  - Define API service deployment goals
2. **Production readiness checklist walkthrough** (15 min)
  - Environment variables, dependency pinning, path/import reliability
  - API runtime conventions and logging
3. **API architecture setup** (15 min)
  - Add minimal service wrapper around existing flow
  - Define request/response schema
4. **Deployment options deep dive** (20 min)
  - Option A: local API service (`uvicorn`)
  - Option B: containerized API deployment
5. **Live-coding: API deployment pipeline** (25 min)
  - Start service and test `GET /health`
  - Call `POST /generate-book` and verify output
6. **Operations and monitoring basics** (10 min)
  - API health checks, request latency, and error triage flow
7. **Capstone demo runbook** (10 min)
  - Student presentation script and API demo sequencing
8. **Quiz + deployment debugging drill** (10 min)
  - Validate understanding of API deployment failure handling
9. **Wrap-up and post-course growth plan** (5 min)
   - Final recommendations and next project extensions

## Learning Objectives (explicit)

By the end of Day 4, learners will be able to:

- Expose the CrewAI book flow through a simple API service.
- Configure FastAPI + Uvicorn startup and runtime environment variables.
- Validate `GET /health` and `POST /generate-book` endpoints.
- Deploy API service locally and optionally in a container.
- Present an end-to-end API capstone demo with troubleshooting confidence.

## Target audience

- Learners who completed Days 1–3 and can run the project locally.
- Developers interested in operationalizing LLM pipelines as services.
- Students preparing portfolio-ready project delivery.

## Prerequisites (detailed)

- Project works locally with outline + chapter generation paths.
- Python environment and API keys already configured.
- Basic familiarity with shell commands, HTTP requests, and optional Docker usage.
- Access to a machine/VM where environment variables can be set securely.

## Setup steps (full commands and checks)

1. Activate virtual environment:

```bash
source .venv/bin/activate
```

2. Confirm core dependencies:

```bash
pip show crewai crewai-tools pydantic fastapi uvicorn
```

3. Export required environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export SERPER_API_KEY="..."
export PYTHONPATH="$PWD"
```

4. Smoke test project locally first:

```bash
python main.py
```

5. Start API service locally:

```bash
uvicorn api_service:app --host 0.0.0.0 --port 8000 --reload
```

6. Test health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

## Detailed Project Orientation (walkthrough)

Day 4 file focus:

- [main.py](main.py): runtime entrypoint and full orchestration path.
- [types.py](types.py): schema contracts used across pipeline.
- [api_service.py](api_service.py): FastAPI app, endpoint routing, request/response handling.
- [crews/outline_book_crew/config/agents.yaml](crews/outline_book_crew/config/agents.yaml): outline behavior settings.
- [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml): outline task constraints.
- [crews/write_book_chapter_crew/config/agents.yaml](crews/write_book_chapter_crew/config/agents.yaml): chapter writer/researcher behavior.
- [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml): chapter quality controls.

Instructor note: Day 4 emphasis is API service reliability and deployment confidence, not feature expansion.

## Deployment Strategy Walkthrough — practical options for this project

### Option A: Local API deployment (recommended for class)

Use this for fastest student success in one class session.

1. Install dependencies including `fastapi` and `uvicorn`.
2. Run `uvicorn api_service:app --host 0.0.0.0 --port 8000`.
3. Test `GET /health`.
4. Send request to `POST /generate-book`.
5. Verify JSON response and generated `.md` artifact.

### Option B: Containerized API deployment (portable option)

Use this when you want consistent runtime across machines.

1. Build image with API server dependencies.
2. Inject API keys at runtime.
3. Run container exposing port `8000`.
4. Call API endpoints from host.
5. Mount volume if artifact persistence is required.

### Option C: Managed hosting (brief mention only)

Use this for production extension after class.

1. Deploy container to a managed platform.
2. Configure secrets via platform secret manager.
3. Add auth/rate limiting before public exposure.

## Live-coding block: Implement API Service Deployment (step-by-step)

Step 0 — Create `api_service.py` with minimal endpoints:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CrewAI Book Generator API")

class GenerateBookRequest(BaseModel):
    title: str
    topic: str
    goal: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate-book")
def generate_book(payload: GenerateBookRequest):
    # call existing flow/service function here
    return {"status": "accepted", "title": payload.title}
```

Step 1 — Add dependencies for API runtime:

```bash
pip install fastapi uvicorn
```

Step 2 — Start API server:

```bash
uvicorn api_service:app --host 0.0.0.0 --port 8000 --reload
```

Step 3 — Test health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Step 4 — Test generation endpoint:

```bash
curl -X POST http://127.0.0.1:8000/generate-book \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI in 2026",
    "topic": "Current state of AI across industries",
    "goal": "Generate a practical multi-chapter book"
  }'
```

Step 5 — Add container deployment for API service:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "api_service:app", "--host", "0.0.0.0", "--port", "8000"]
```

Step 6 — Build and run container:

```bash
docker build -t crewai-book-api:latest .
docker run --rm \
  -p 8000:8000 \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e SERPER_API_KEY="$SERPER_API_KEY" \
  crewai-book-api:latest
```

Step 7 — Validate service after deployment:

```bash
curl http://127.0.0.1:8000/health
```

Step 8 — Keep Day 4 service simple (synchronous endpoint first).

## Speaker Notes & Teaching Tips

- Keep Day 4 scoped to one success path: `health` + `generate-book`.
- Explain clearly that synchronous endpoint is chosen for teaching simplicity.
- Use a fixed payload for repeatable demo results.
- Mention background jobs as an advanced extension, not a Day 4 requirement.

## Deep-dive: API Operations, Logging, and Recovery Basics

Explain minimal operations model:

1. Validate secrets at startup.
2. Start API server and capture logs.
3. Verify health endpoint and generation endpoint behavior.
4. Verify output artifact (if file save remains enabled) exists and is non-empty.
4. If failure occurs, triage by layer:
   - env/config,
  - API routing/validation,
  - dependency/import,
  - model/tool call,
  - output assembly/write.

Introduce simple recovery policy:

- Fail fast for missing keys.
- Use clear HTTP error responses on invalid input.
- Preserve logs for failed API requests.

## Troubleshooting Checklist (common errors and fixes)

- API server fails to start due to missing package
  - Install `fastapi` and `uvicorn` in active environment.

- API request returns `422 Unprocessable Entity`
  - Check JSON payload fields and types against request schema.

- `POST /generate-book` is too slow or times out
  - Reduce chapter scope for class demo and keep synchronous mode for MVP.

- Docker build fails due to dependency issues
  - Regenerate `requirements.txt` and rebuild with clean cache.

- Container runs but API not reachable
  - Verify `-p 8000:8000` port mapping and container logs.

- API/auth failures in deployed environment
  - Verify secrets are passed at runtime and not hardcoded.

- Runtime import path errors
  - Ensure `PYTHONPATH` is set correctly inside deployment environment.

## Short Quiz (answers included)

Q1: Why should deployment runs validate required environment variables at startup?

- Answer: To fail early with clear diagnostics instead of producing partial or misleading runs.

Q2: What are the two MVP endpoints taught on Day 4?

- Answer: `GET /health` and `POST /generate-book`.

Q3: What is the main advantage of container deployment for this project?

- Answer: Environment consistency and portability across machines.

Q4: What must be validated before calling `POST /generate-book`?

- Answer: JSON payload shape (`title`, `topic`, `goal`) and required API keys.

Q5: Why is synchronous endpoint mode acceptable for Day 4?

- Answer: It keeps the teaching flow simple and understandable; background jobs can be introduced later.

Q6: What must be persisted after a deployment run?

- Answer: Generated markdown artifacts and relevant logs.

## Exercises / Try It Yourself (expanded — many step-by-step tasks)

Exercise 1 — Build a reproducible run checklist (beginner, 15–20 min)

- Goal: Produce a one-page checklist for local API service runs.
- Steps:
  1. List dependencies, env vars, and `uvicorn` startup command.
  2. Add endpoint verification steps (`/health`, `/generate-book`).
  3. Add top 3 failure/recovery actions.

Exercise 2 — Harden request validation (intermediate, 20 min)

- Goal: Improve API request validation and error responses.
- Steps:
  1. Add stricter request model fields.
  2. Return meaningful 4xx messages on invalid input.
  3. Test invalid and valid requests.

Exercise 3 — Containerized API run (intermediate, 20–30 min)

- Goal: Run API service inside Docker and hit it from host.
- Steps:
  1. Build Docker image.
  2. Run with env vars and `-p 8000:8000`.
  3. Validate endpoint response from host.

Exercise 4 — Basic API smoke test script (advanced, 25–35 min)

- Goal: Automate service health + generation endpoint checks.
- Steps:
  1. Assert `/health` returns `status=ok`.
  2. Send sample generate request.
  3. Assert non-empty response fields.

Exercise 5 — Capstone demo runbook (optional, 20 min)

- Goal: Create a polished API demo flow for final presentation.
- Steps:
  1. Define fixed request payload.
  2. Prepare expected endpoint outputs and timing.
  3. Add backup plan for API/tool downtime.

## Expected outputs and validation

After Day 4 completion, learners should verify:

- API service runs via repeatable startup command.
- `GET /health` returns successful readiness response.
- `POST /generate-book` accepts valid payload and returns useful output.
- Container path (if used) serves API on mapped port.
- Students can deliver a stable end-to-end API demo.

## Example full code snippets (copyable)

Minimal API service (`api_service.py`):

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CrewAI Book Generator API")

class GenerateBookRequest(BaseModel):
  title: str
  topic: str
  goal: str

@app.get("/health")
def health():
  return {"status": "ok"}

@app.post("/generate-book")
def generate_book(payload: GenerateBookRequest):
  # integrate existing flow kickoff here
  return {
    "status": "accepted",
    "title": payload.title,
    "message": "Generation started"
  }
```

API run command:

```bash
uvicorn api_service:app --host 0.0.0.0 --port 8000 --reload
```

Minimal Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "api_service:app", "--host", "0.0.0.0", "--port", "8000"]
```

Basic API smoke-test script:

```bash
#!/usr/bin/env bash
set -euo pipefail

health=$(curl -s http://127.0.0.1:8000/health)
echo "$health" | grep -q '"status":"ok"\|"status": "ok"'

response=$(curl -s -X POST http://127.0.0.1:8000/generate-book \
  -H "Content-Type: application/json" \
  -d '{"title":"AI in 2026","topic":"AI trends","goal":"Generate a short book"}')

if [[ -z "${response:-}" ]]; then
  echo "Empty response from /generate-book"
  exit 1
fi

echo "API smoke test passed"
```

## Troubleshooting (expanded with examples)

- Error: `docker: command not found`
  - Cause: Docker not installed or not in PATH.
  - Fix: Install Docker Desktop and confirm daemon is running.

- Error: `404 Not Found` on API route
  - Cause: wrong path or server started with wrong app module.
  - Fix: verify route path and run `uvicorn api_service:app ...`.

- Error: `422` when posting JSON
  - Cause: missing required fields in payload.
  - Fix: send `title`, `topic`, and `goal` with correct types.

- Error: API call is very slow
  - Cause: full chapter generation is compute/network heavy.
  - Fix: use smaller scope for class demo and explain background-job extension.

## Homework (post-course capstone)

- Prepare a complete API deployment handoff package (startup command + env checklist + smoke test).
- Record one 5-minute capstone API demo (`/health` + `/generate-book`).
- Write one improvement proposal for production hardening (auth, retries, or background jobs).

## Advanced topics to mention (briefly, for curious learners)

- API authentication and rate limiting.
- Background job queue for long-running generation requests.
- Multi-environment deployment (dev/stage/prod) for API services.

## Glossary

- API service: application exposed through HTTP endpoints.
- Smoke test: quick check that core service behavior works after deployment.
- Stateless container: container that does not persist mutable runtime state internally.
- Runbook: documented sequence of steps to operate and troubleshoot a system.

## Additional resources

- Docker docs: https://docs.docker.com
- FastAPI docs: https://fastapi.tiangolo.com
- Uvicorn docs: https://www.uvicorn.org
- CrewAI docs: https://docs.crewai.com

## Full checklist for the instructor

1. Verify local baseline run before deployment demo.
2. Demonstrate API service startup (`uvicorn`) end-to-end.
3. Demonstrate `GET /health` and `POST /generate-book` live.
4. Demonstrate optional containerized API path.
5. Run quiz and one deployment exercise.
6. Complete capstone API demo handoff and post-course guidance.

---

Files referenced in this lesson:
- [main.py](main.py)
- [types.py](types.py)
- [api_service.py](api_service.py)
- [crews/outline_book_crew/config/agents.yaml](crews/outline_book_crew/config/agents.yaml)
- [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml)
- [crews/write_book_chapter_crew/config/agents.yaml](crews/write_book_chapter_crew/config/agents.yaml)
- [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml)
