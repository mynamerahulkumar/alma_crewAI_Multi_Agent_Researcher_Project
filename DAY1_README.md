# Day 1 — CrewAI Multi-Agent Foundations (2-hour live coding)

## 🎯 Title & Topic
CrewAI & Project Foundations — Build and Run the Book Outline Pipeline

## Overview (long form)

This Day 1 module is designed to give learners a deep, hands-on foundation in the current CrewAI multi-agent repository, the flow orchestration pattern used in this project, and the minimal steps required to run the first production path end-to-end: generate a structured book outline from a topic and goal.

The session is structured for a 2-hour live coding class with checkpoints, interactive exercises, and a practical mini-project. Students will understand how `Flow` state moves across listeners, how crews map to `agents.yaml` and `tasks.yaml`, and how typed outputs (`Pydantic`) are used to keep the pipeline reliable.

This lesson follows the same instructional structure as your reference Day 1 format and is written so an instructor can present, code live, run, debug, and iterate with students. Sections include: session flow, objectives, minute-by-minute plan, speaker notes, file walkthroughs, step-by-step live coding, quiz with answers, troubleshooting, homework, glossary, and advanced topics.

This project is taught over 4 days. Day 1 focuses only on foundations + outline generation. Days 2–4 continue with chapter generation concurrency, output quality hardening, and production readiness.

## **SESSION FLOW**

### **What We'll Cover Today (Step-by-Step)**

1. **Welcome, 4-day roadmap & learning outcomes** (10 min)
   - Quick introductions and expectations
   - Explain how Day 1 fits into the 4-day progression
2. **Repository orientation & architecture walkthrough** (15 min)
   - Walk top-level files and crew folders
   - Explain data contracts, crews, and flow listeners
3. **Environment setup & dependency checks** (15 min)
   - Virtual environment setup
   - Install required libraries and set API keys
4. **Core data model deep dive: `types.py`** (10 min)
   - Explain `ChapterOutline`, `BookOutline`, `Chapter`
   - Why typed outputs matter for multi-agent pipelines
5. **Outline crew deep dive** (20 min)
   - Read `outline_crew.py`, `agents.yaml`, `tasks.yaml`
   - Explain sequential process and output schema mapping
6. **Flow orchestration deep dive: `main.py`** (20 min)
   - Explain `@start`, `@listen`, state transitions
   - Identify outline generation, chapter writing, final save steps
7. **Live-coding: run only the outline stage safely** (20 min)
   - Execute outline generation path
   - Inspect typed output and discuss quality checks
8. **Quiz, debugging drill & common pitfalls** (5 min)
   - Run short interactive Q&A
   - Demonstrate fixes for import/env/tooling issues
9. **Wrap-up, exercises & Day 2 preview** (5 min)
   - Assign practical tasks
   - Preview concurrent chapter generation for Day 2

## Learning Objectives (explicit)

By the end of Day 1, learners will be able to:

- Explain the repository layout and responsibilities of main files and crew folders.
- Describe how CrewAI agents, tasks, and crews are configured using YAML.
- Run the outline generation workflow and inspect structured outputs.
- Explain how typed models (`Pydantic`) enforce output shape consistency.
- Identify and fix common environment/configuration issues in this project.

## Target audience

- Developers with intermediate Python skills.
- Learners comfortable with virtual environments and package installation.
- Learners new to CrewAI are welcome; prior LLM orchestration knowledge is helpful but not required.

## Prerequisites (detailed)

- Python 3.10+ recommended.
- Ability to create and activate a virtual environment.
- API credentials for LLM/tooling (for this project, typically OpenAI-compatible model access and Serper search key if search tools are used).
- Basic familiarity with YAML and JSON-like structured outputs.

## Setup steps (full commands and checks)

1. Create and activate a virtual environment (macOS example):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install required dependencies (minimal Day 1 set):

```bash
pip install --upgrade pip
pip install crewai crewai-tools pydantic
```

3. Set environment variables for model/tool access (example):

```bash
export OPENAI_API_KEY="sk-..."
export SERPER_API_KEY="..."
```

4. Because imports use the package path `write_a_book_with_flows`, ensure the project is importable:

```bash
export PYTHONPATH="$PWD"
```

5. Run the project entrypoint:

```bash
python main.py
```

6. Confirm expected behavior:
   - Outline generation starts.
   - Chapter tasks may run next depending on flow path.
   - A markdown file is created when the full flow completes.

Instructor note: For Day 1, focus on successfully running and validating the outline phase first.

## Detailed Project Orientation (walkthrough)

Open these files in sequence and explain responsibilities:

- [main.py](main.py): main orchestration flow, state definition, listeners, final markdown save.
- [types.py](types.py): typed output contracts (`ChapterOutline`, `BookOutline`, `Chapter`).
- [crews/outline_book_crew/outline_crew.py](crews/outline_book_crew/outline_crew.py): outline crew class, agents/tasks wiring, `output_pydantic=BookOutline`.
- [crews/outline_book_crew/config/agents.yaml](crews/outline_book_crew/config/agents.yaml): role/goal/backstory prompts for `researcher` and `outliner`.
- [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml): research + outline task definitions and expected outputs.
- [crews/write_book_chapter_crew/write_book_chapter_crew.py](crews/write_book_chapter_crew/write_book_chapter_crew.py): chapter crew structure (preview for Day 2).
- [crews/write_book_chapter_crew/config/agents.yaml](crews/write_book_chapter_crew/config/agents.yaml): chapter researcher/writer prompt configs.
- [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml): chapter research/writing task contracts.

Instructor note: Highlight how prompt engineering is externalized in YAML, while orchestration is in Python.

## Core Data Model Deep Dive — `types.py`

Walk line-by-line through `types.py`:

1. `ChapterOutline`: one chapter title + description.
2. `BookOutline`: list of chapter outlines.
3. `Chapter`: final chapter content.

Teaching points:

- Why typed contracts reduce ambiguity in agent outputs.
- How `output_pydantic` in crew tasks enforces schema.
- Why this is important before introducing concurrency.

## Outline Crew Walkthrough — `outline_crew.py` + YAML configs

Open `crews/outline_book_crew/outline_crew.py` and explain:

- `@CrewBase` pattern and how it loads `agents_config` and `tasks_config`.
- `llm = LLM(model="gpt-4o")` central model configuration.
- `researcher` agent using `SerperDevTool()` for research.
- `generate_outline` task returning `output_pydantic=BookOutline`.
- `Process.sequential` ordering (research first, then outlining).

Then connect this to YAML:

- `agents.yaml`: behavior/purpose of each agent.
- `tasks.yaml`: explicit instructions, constraints (e.g., no duplicate chapters), expected output shape.

Instructor tip: Ask students where they would change behavior fastest: Python class vs YAML prompt.

## Flow Orchestration Walkthrough — `main.py`

Open `main.py` and explain flow lifecycle:

1. `BookState`: single source of truth for topic, goal, outline, and chapters.
2. `@start()` -> `generate_book_outline()`:
   - Runs `OutlineCrew().crew().kickoff(...)`.
   - Saves `chapters` into `self.state.book_outline`.
3. `@listen(generate_book_outline)` -> `write_chapters()`:
   - Creates async tasks for each chapter outline.
   - Calls `WriteBookChapterCrew` for each chapter.
4. `@listen(write_chapters)` -> `join_and_save_chapter()`:
   - Joins chapter markdown.
   - Saves final book file.

Instructor note: Day 1 is foundation day—teach full flow structure, but execute and verify outline-first before deeper async analysis.

## Live-coding block: Run the Outline Stage (step-by-step)

We will code/run in small checkpoints so learners can follow confidently.

Step 0 — Environment check:

```bash
python -V
pip -V
```

Step 1 — Confirm install + keys:

```bash
pip show crewai crewai-tools pydantic
env | grep -E "OPENAI_API_KEY|SERPER_API_KEY"
```

Step 2 — Add temporary debug print in `generate_book_outline()` (if needed):

```python
print("Inputs:", {"topic": self.state.topic, "goal": self.state.goal[:120]})
```

Step 3 — Run the flow:

```bash
python main.py
```

Step 4 — Validate outline output in logs:

- Confirm `Kickoff the Book Outline Crew` appears.
- Confirm a list of chapters is printed.
- Confirm chapter entries have title + description.

Step 5 — (Optional controlled demo) stop after outline stage for Day 1 focus:

- Temporarily comment out chapter writing listener invocation path while teaching basics.
- Re-enable it after conceptual clarity.

## Speaker Notes & Teaching Tips

- Emphasize why we separate orchestration logic (Python) and behavior definitions (YAML).
- Keep students focused on one success path first: valid structured outline.
- Pause after each checkpoint and ask students to predict next output.
- Explain that multi-agent reliability starts with strict output contracts, not just prompts.

## Deep-dive: State, Typed Outputs, and Reliability

Discuss these key ideas:

- State continuity: all listeners operate on `self.state`.
- Typed outputs prevent downstream breakage from malformed content.
- Prompt constraints in YAML improve consistency (chapter length limits, no duplication).
- Reliability strategy for multi-agent systems:
  1. Define schema first.
  2. Enforce schema in task outputs.
  3. Add validation/logging before fan-out concurrency.

## Troubleshooting Checklist (common errors and fixes)

- `ModuleNotFoundError: No module named 'write_a_book_with_flows'`
  - Ensure project root is in `PYTHONPATH`.
  - Run commands from project root directory.

- Missing API key / auth failure
  - Re-check exported environment variables.
  - Confirm key is active and not expired.

- Serper tool errors
  - Verify `SERPER_API_KEY` is set.
  - Temporarily test without search-dependent steps if necessary.

- Pydantic output parsing issues
  - Check task prompt clarity in YAML.
  - Ensure `output_pydantic` matches expected task result structure.

- Async chapter writing confusion
  - Day 1 scope: explain structure, deeply debug concurrency on Day 2.

## Short Quiz (answers included)

Q1: Which file defines the flow lifecycle and listeners?

- Answer: `main.py`

Q2: Which file defines the chapter and outline schemas?

- Answer: `types.py`

Q3: What does `output_pydantic=BookOutline` achieve?

- Answer: It enforces that crew task output matches the `BookOutline` schema.

Q4: Where are role/goal/backstory prompts configured for outline agents?

- Answer: `crews/outline_book_crew/config/agents.yaml`

Q5: Why is Day 1 focused on outline-first validation before full chapter generation?

- Answer: It isolates fundamentals (state + schema + prompts) and reduces debugging complexity before concurrency.

## Exercises / Try It Yourself (expanded — many step-by-step tasks)

Exercise 1 — Change topic and goal safely (beginner, 15–20 min)

- Goal: Update `BookState.topic` and `BookState.goal` to a new domain and run outline generation.
- Steps:
  1. Edit topic/goal in `main.py`.
  2. Run `python main.py`.
  3. Check whether generated chapter sequence is coherent.

Exercise 2 — Improve outline quality with task constraints (intermediate, 20–30 min)

- Goal: Refine `generate_outline` prompt to enforce stronger chapter ordering and coverage.
- Steps:
  1. Open `crews/outline_book_crew/config/tasks.yaml`.
  2. Add explicit constraints (e.g., intro -> fundamentals -> applications -> risks -> future).
  3. Re-run and compare chapter quality before/after.

Exercise 3 — Add basic validation logging (intermediate, 20 min)

- Goal: Print chapter count + missing field checks after outline generation.
- Steps:
  1. In `generate_book_outline()`, add validation loop over chapters.
  2. Warn if title/description missing.
  3. Re-run and inspect logs.

Exercise 4 — Tune agent intent through YAML (advanced, 25–35 min)

- Goal: Make `researcher` and `outliner` produce less overlap and more practical chapter plans.
- Steps:
  1. Edit `agents.yaml` goals/backstories.
  2. Keep task prompt unchanged.
  3. Compare outline diversity and duplication risk.

Exercise 5 — Dry-run chapter crew input prep (optional, 20 min)

- Goal: Inspect payload passed into chapter crew without writing full chapters.
- Steps:
  1. Add debug print for `chapter_title`, `chapter_description`, and `book_outline` payload in `write_chapters()`.
  2. Run once and verify payload quality.
  3. Remove debug logs after validation.

## Expected outputs and validation

After Day 1 live coding and exercises, learners should verify:

- The outline crew runs successfully from `main.py`.
- Output contains structured chapter objects with title + description.
- Students can explain how YAML config maps to agent behavior.
- Students can identify where to modify flow logic vs prompt/task logic.

## Example full code snippets (copyable)

Minimal outline-only debug runner pattern:

```python
from write_a_book_with_flows.crews.outline_book_crew.outline_crew import OutlineCrew

inputs = {
    "topic": "AI in healthcare in 2026",
    "goal": "Create a practical beginner-to-advanced book roadmap"
}

output = OutlineCrew().crew().kickoff(inputs=inputs)
chapters = output["chapters"]

for index, chapter in enumerate(chapters, start=1):
    print(index, chapter.title, "-", chapter.description)
```

Basic validation helper (optional utility function):

```python
def validate_outline(chapters):
    issues = []
    for index, chapter in enumerate(chapters, start=1):
        if not getattr(chapter, "title", "").strip():
            issues.append(f"Chapter {index} missing title")
        if not getattr(chapter, "description", "").strip():
            issues.append(f"Chapter {index} missing description")
    return issues
```

## Troubleshooting (expanded with examples)

- Error: `TypeError` when reading output fields
  - Cause: assuming dict shape while receiving typed objects.
  - Fix: inspect object type and use attribute access consistently.

- Error: model/provider mismatch
  - Cause: configured model unavailable for current credentials.
  - Fix: align model name in crew class with available provider model.

- Error: low-quality repetitive outlines
  - Cause: weak task constraints.
  - Fix: tighten `generate_outline` instructions and add anti-duplication constraints.

- Error: chapter fan-out too costly for demo
  - Cause: full pipeline runs many LLM calls.
  - Fix: keep Day 1 to outline-only run and postpone chapter generation depth.

## Homework (before Day 2)

- Complete at least two exercises from Day 1.
- Produce two different outlines using two different `topic/goal` pairs.
- Submit a short reflection: what changed most when you edited YAML vs Python?
- Prepare one question on async fan-out in `write_chapters()` for Day 2.

## Advanced topics to mention (briefly, for curious learners)

- Agent specialization trade-offs: fewer generalized agents vs more specialized agents.
- Structured output validation and retry loops for robust pipelines.
- Concurrency patterns in multi-agent writing workflows.

## Glossary

- Flow: orchestration object that coordinates stateful execution steps.
- Crew: group of agents + tasks executed with a defined process.
- Agent: role-driven LLM worker with goals, backstory, and optional tools.
- Task: unit of work assigned to an agent.
- output_pydantic: schema enforcement for structured task outputs.
- Listener: function triggered after a previous flow step completes.

## Additional resources

- CrewAI docs: https://docs.crewai.com
- Pydantic docs: https://docs.pydantic.dev
- Python asyncio docs: https://docs.python.org/3/library/asyncio.html

## Full checklist for the instructor

1. Confirm environment setup and keys before class starts.
2. Walk all core files in the Day 1 orientation order.
3. Run and validate outline generation live.
4. Demonstrate one YAML prompt edit and one Python flow edit.
5. Complete quiz + at least one student exercise.
6. Assign homework and preview Day 2 concurrency deep dive.

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
