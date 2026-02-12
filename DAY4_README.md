# Day 4 — CLI-First Deployment & Optional API Delivery (2-hour live coding)

## 🎯 Title & Topic
Productionizing the Multi-Agent Book Pipeline — Deploy with CLI as Primary, FastAPI as Optional Secondary Path

## Overview (long form)

Day 4 completes the learning arc by moving from development workflows to deployment-ready operation. The primary path is CLI-first: run the existing flow in `main.py`, validate outputs, and package a repeatable runtime command sequence that works on local machines, remote VMs, and lightweight schedulers.

This session is intentionally practical and constrained to a 2-hour classroom format. Students will standardize environment setup, run full generation through the existing pipeline, validate markdown artifacts, and apply operational checks for reliability.

An optional secondary path introduces a minimal FastAPI wrapper for occasional API usage. This path is additive and does not replace the CLI flow. The core system of record remains orchestration in `main.py`.

By the end of the session, learners can confidently deploy and operate this project from the command line, and optionally expose a thin API endpoint for demos or integration.

## **SESSION FLOW**

### **What We'll Cover Today (Step-by-Step)**

1. **Recap Days 1–3 and Day 4 outcomes** (10 min)
   - Confirm foundations: schema, fan-out, output assembly
   - Define Day 4 goal: operational reliability
2. **CLI deployment architecture walkthrough** (15 min)
   - Trace production path in `main.py`
   - Validate data contracts from `types.py`
3. **Configuration and prompt surfaces review** (15 min)
   - Review YAML files used at runtime
   - Discuss safe production edits
4. **Technical deep dive: runtime hardening** (20 min)
   - Environment checks, logging, repeatable commands
   - Output verification and failure handling
5. **Live coding: deploy and run CLI flow end-to-end** (30 min)
   - Execute generation pipeline
   - Validate resulting markdown artifact
6. **Optional secondary path: FastAPI adapter** (15 min)
   - Add minimal API wrapper without changing core flow
   - Demonstrate one request cycle
7. **Troubleshooting + quiz + capstone demo script** (10 min)
   - Rapid failure triage practice
   - Short concept checks
8. **Wrap-up, homework, and post-course growth path** (5 min)

## Learning Objectives (explicit)

By the end of Day 4, learners will be able to:

- Deploy and run the full project using a CLI-first workflow.
- Validate execution dependencies and environment variables.
- Explain how `main.py` orchestrates outline, chapter writing, and save.
- Identify where behavior is controlled in YAML config files.
- Use an optional FastAPI wrapper as a secondary access path.
- Troubleshoot common deployment/runtime failures quickly.

## Target audience

- Learners who completed Days 1–3.
- Python developers comfortable with terminal-based workflows.
- Teams needing practical, low-overhead deployment for agent pipelines.

## Prerequisites (detailed)

- Python 3.10+ installed.
- Working virtual environment and dependency installation.
- Valid model/tool API keys.
- Ability to run terminal commands from project root.
- Prior understanding of:
  - `main.py` flow lifecycle
  - `types.py` output models
  - crew/task YAML configuration files

## Setup steps (full commands and checks)

1. Activate virtual environment:

```bash
source .venv/bin/activate
```

2. Confirm core dependencies:

```bash
pip show crewai crewai-tools pydantic
```

3. Export required environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export SERPER_API_KEY="..."
export PYTHONPATH="$PWD"
```

4. Optional: save reusable runtime env file:

```bash
cat > .env.runtime <<'EOF'
export OPENAI_API_KEY="sk-..."
export SERPER_API_KEY="..."
export PYTHONPATH="$PWD"
EOF
```

5. Smoke-test primary CLI flow:

```bash
python main.py
```

6. Confirm markdown artifact is created in project root.

## Detailed Project Orientation (walkthrough)

Review files in this order:

- [main.py](main.py): canonical runtime entrypoint and orchestration (`generate_book_outline` → `write_chapters` → `join_and_save_chapter`).
- [types.py](types.py): strict output contracts (`ChapterOutline`, `BookOutline`, `Chapter`).
- [crews/outline_book_crew/outline_crew.py](crews/outline_book_crew/outline_crew.py): outline crew wiring and `output_pydantic=BookOutline`.
- [crews/outline_book_crew/config/agents.yaml](crews/outline_book_crew/config/agents.yaml): outline agent behavior.
- [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml): outline task constraints.
- [crews/write_book_chapter_crew/write_book_chapter_crew.py](crews/write_book_chapter_crew/write_book_chapter_crew.py): chapter crew wiring and `output_pydantic=Chapter`.
- [crews/write_book_chapter_crew/config/agents.yaml](crews/write_book_chapter_crew/config/agents.yaml): chapter agent behavior.
- [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml): chapter output constraints.

Instructor note: keep `main.py` as the source of truth. API is optional and should call existing flow logic.

## CLI Runtime Deep Dive — `main.py` as deployment contract

- Entrypoint: `python main.py`
- Flow lifecycle:
  1. Build outline via `OutlineCrew`
  2. Generate chapters concurrently via `WriteBookChapterCrew`
  3. Join and save markdown artifact
- Deployment rule for class: if CLI path is stable, system is deployable.

## Config Deep Dive — YAML controls without orchestration changes

- Prompt and task behavior lives in YAML files.
- Safer production tuning order:
  1. edit `tasks.yaml` constraints,
  2. then `agents.yaml` style/role guidance,
  3. avoid frequent orchestration edits in `main.py`.

## Deployment Strategy Walkthrough — practical options for this project

### Option A: CLI local/VM deployment (recommended primary)

1. Activate env and export keys.
2. Run `python main.py`.
3. Validate logs and markdown output.
4. Repeat with reusable env file/script.
5. Use this as classroom and production baseline.

### Option B: CLI containerized deployment (portable)

1. Build image with Python + dependencies.
2. Inject keys at runtime.
3. Run container executing `python main.py`.
4. Mount volume for output artifacts.
5. Keep image stateless and persist outputs externally.

### Option C: Optional API adapter (secondary path)

1. Add thin `api_service.py` wrapper.
2. Keep endpoint logic calling existing flow.
3. Use for occasional integrations, not as primary course runtime.

## Live-coding block: Implement Deployment Steps (step-by-step)

### Part A — Primary CLI deployment

Step 0 — Confirm runtime context:

```bash
python -V
which python
pwd
```

Step 1 — Validate environment and keys:

```bash
source .venv/bin/activate
env | grep -E "OPENAI_API_KEY|SERPER_API_KEY|PYTHONPATH"
```

Step 2 — Run canonical flow:

```bash
python main.py
```

Step 3 — Verify artifact:

```bash
ls -1 *.md
head -n 40 *.md
grep -n "^# " *.md
```

Step 4 — Package repeatable run command:

```bash
source .venv/bin/activate && source .env.runtime && python main.py
```

### Part B — Optional API adapter (secondary)

Step 5 — Install API libraries only if needed:

```bash
pip install fastapi uvicorn
```

Step 6 — Create `api_service.py` thin wrapper calling existing flow.

Step 7 — Run optional API service:

```bash
uvicorn api_service:app --host 0.0.0.0 --port 8000 --reload
```

Step 8 — Test optional endpoints:

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/generate-book \
  -H "Content-Type: application/json" \
  -d '{"title":"AI in 2026","topic":"AI trends","goal":"Generate a practical guide"}'
```

Instructor note: if time is limited, complete Part A only and keep Part B conceptual.

## Speaker Notes & Teaching Tips

- Reiterate throughout: CLI is the production baseline for this course.
- Use one stable topic/goal payload for reproducible results.
- Demonstrate one failure and one fix live (missing env var is ideal).
- Keep API section short and optional; avoid framework deep dives.

## Deep-dive: Operations, Logging, and Recovery Basics

Minimal operations model:

1. Validate secrets at startup.
2. Run CLI flow and capture logs.
3. Verify output artifact exists and is non-empty.
4. Triage failures by layer:
   - env/config,
   - dependency/import,
   - model/tool call,
   - output assembly/write.

Recovery policy:

- Fail fast for missing keys.
- Retry once for transient external errors.
- Preserve logs for debugging.

## Troubleshooting Checklist (common errors and fixes)

- `ModuleNotFoundError` for project imports
  - Run from repo root and export `PYTHONPATH="$PWD"`.

- Missing API keys / auth failures
  - Re-export `OPENAI_API_KEY` and `SERPER_API_KEY`.

- No markdown output generated
  - Check exceptions in chapter generation and save stage.
  - Confirm write permissions in project directory.

- Runtime slow or unstable
  - Reduce chapter scope for classroom runs.

- Optional API returns but no generation occurs
  - Ensure endpoint calls flow logic from `main.py`.

## Short Quiz (answers included)

Q1: What is the primary deployment path for Day 4?

- Answer: CLI execution using `python main.py`.

Q2: Which file contains end-to-end orchestration?

- Answer: `main.py`.

Q3: Which file defines strict output contracts?

- Answer: `types.py`.

Q4: Where should behavior tuning happen first?

- Answer: YAML task/agent configs under `crews/*/config/`.

Q5: Is FastAPI required for Day 4 success?

- Answer: No, it is optional.

## Exercises / Try It Yourself (expanded — many step-by-step tasks)

Exercise 1 — Build one-command CLI run script (beginner, 15 min)

- Goal: Execute full flow with one command.
- Steps:
  1. Create `run_day4.sh`.
  2. Activate env, source runtime vars, run `python main.py`.
  3. Verify markdown output.

Exercise 2 — Failure injection and recovery (intermediate, 20 min)

- Goal: Practice deployment debugging.
- Steps:
  1. Unset one API key and run.
  2. Capture root-cause error.
  3. Restore key and rerun successfully.

Exercise 3 — YAML tuning for output consistency (intermediate, 20 min)

- Goal: Improve repeatability.
- Steps:
  1. Edit chapter task constraints in [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml).
  2. Re-run CLI flow.
  3. Compare output structure quality.

Exercise 4 — Optional API wrapper drill (advanced, 20–25 min)

- Goal: Expose minimal endpoint without changing core flow.
- Steps:
  1. Implement thin FastAPI adapter.
  2. Add `/health` and `/generate-book`.
  3. Trigger one generation and verify output.

## Expected outputs and validation

After Day 4 completion, learners should verify:

- CLI run `python main.py` completes end-to-end.
- A markdown artifact is generated in project root.
- Logs show outline generation, chapter writing, and save completion.
- Students can identify files controlling behavior and reliability.
- Optional: API endpoint triggers same flow for occasional use.

## Example full code snippets (copyable)

CLI-first run wrapper:

```bash
#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
source .env.runtime
python main.py
```

Optional FastAPI thin adapter:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from main import kickoff

app = FastAPI(title="Optional CrewAI Adapter")

class GenerateRequest(BaseModel):
    title: str | None = None
    topic: str | None = None
    goal: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate-book")
def generate_book(_: GenerateRequest):
    kickoff()
    return {"status": "completed", "mode": "cli-flow-invoked"}
```

## Troubleshooting (expanded with examples)

- Error: `No module named 'write_a_book_with_flows'`
  - Cause: import path not resolved.
  - Fix: run from repo root and set `PYTHONPATH="$PWD"`.

- Error: malformed outline output
  - Cause: weak constraints in [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml).
  - Fix: tighten schema/structure instructions.

- Error: chapter fields missing
  - Cause: output mismatch vs `Chapter` model.
  - Fix: strengthen output instructions in [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml).

- Error: optional API responds but generation stale
  - Cause: adapter not mapping runtime values correctly.
  - Fix: wire payload fields into flow state before kickoff.

## Homework (post-course capstone)

- Create a repeatable CLI deployment runbook for your machine/VM.
- Run two production-style topics and compare output quality.
- Add one reliability enhancement in [main.py](main.py) (logging, validation, or safer save behavior).
- Optional: complete API adapter and document when to use it vs CLI.

## Advanced topics to mention (briefly, for curious learners)

- Queue-based asynchronous API execution.
- Retry policy for failed chapter tasks.
- Structured run metadata and observability dashboards.
- Artifact versioning and external storage backends.

## Glossary

- CLI-first deployment: operating system primarily via terminal commands.
- Orchestration flow: ordered runtime stages in `main.py`.
- Typed output contract: schema-enforced output via Pydantic models.
- Thin API adapter: minimal HTTP layer that calls existing flow logic.

## Additional resources

- CrewAI docs: https://docs.crewai.com
- Pydantic docs: https://docs.pydantic.dev
- Python asyncio docs: https://docs.python.org/3/library/asyncio.html
- FastAPI docs (optional): https://fastapi.tiangolo.com

## Full checklist for the instructor

1. Confirm every learner can run `python main.py`.
2. Validate environment variables before live run.
3. Walk deployment-relevant files in orientation order.
4. Complete one full CLI run and inspect output.
5. Run troubleshooting drill with one intentional failure.
6. Deliver quiz and one hands-on exercise.
7. Cover optional API adapter only after CLI success.

---

Files referenced in this lesson:
- [main.py](main.py)
- [types.py](types.py)
- [crews/outline_book_crew/outline_crew.py](crews/outline_book_crew/outline_crew.py)
- [crews/outline_book_crew/config/agents.yaml](crews/outline_book_crew/config/agents.yaml)
- [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml)
- [crews/write_book_chapter_crew/write_book_chapter_crew.py](crews/write_book_chapter_crew/write_book_chapter_crew.py)
- [crews/write_book_chapter_crew/config/agents.yaml](crews/write_book_chapter_crew/config/agents.yaml)
- [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml)
