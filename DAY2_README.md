# Day 2 — CrewAI Chapter Generation & Concurrency (2-hour live coding)

## 🎯 Title & Topic
From Outline to Full Chapters — Async Fan-out, Chapter Crew Quality, and Reliable Aggregation

## Overview (long form)

This Day 2 module moves students from foundation-level understanding (Day 1) to production-style chapter generation. The class focuses on how a validated outline is transformed into full chapter drafts using a second crew, with async fan-out in the flow and structured chapter outputs.

Students will trace how each `ChapterOutline` item becomes a task input for `WriteBookChapterCrew`, how multiple chapter jobs are scheduled concurrently via `asyncio.create_task`, and how results are collected and merged into final markdown-ready state.

The session is designed for a 2-hour live coding format with clear checkpoints, progressive debugging, and practical exercises. Learners will improve chapter quality by tuning YAML task constraints and validating chapter cohesion against the overall book goal.

This lesson keeps the same instructional format as Day 1, including session flow, objectives, setup checks, guided walkthroughs, live coding, quiz, troubleshooting, exercises, homework, and instructor checklist.

## **SESSION FLOW**

### **What We'll Cover Today (Step-by-Step)**

1. **Recap Day 1 and define Day 2 outcomes** (10 min)
   - Review outline-first success criteria
   - Introduce Day 2 goals: chapter fan-out + quality control
2. **Review chapter crew architecture** (15 min)
   - Inspect `write_book_chapter_crew.py`
   - Map agents/tasks to chapter writing behavior
3. **Inputs deep dive: chapter payload assembly** (15 min)
   - Analyze how `chapter_title`, `chapter_description`, `book_outline`, and `goal` are passed
   - Explain why payload quality determines output quality
4. **Async flow deep dive: `write_chapters()`** (20 min)
   - Explain `asyncio.create_task` and `asyncio.gather`
   - Discuss ordering, failures, and retry opportunities
5. **Chapter quality constraints in YAML** (15 min)
   - Tune `tasks.yaml` for coherence and reduced duplication
   - Align chapter style with global book objective
6. **Live-coding: run chapter generation with guardrails** (25 min)
   - Add logging/validation checkpoints
   - Run flow and inspect generated chapter objects
7. **Aggregation walkthrough: prepare for final save** (10 min)
   - Ensure chapter titles/content are clean and ordered
   - Validate readiness for Day 3 publishing improvements
8. **Quiz + debugging drill** (5 min)
   - Validate understanding of async fan-out and schema reliability
9. **Wrap-up, assignments & Day 3 preview** (5 min)
   - Assign quality-focused exercises
   - Preview output post-processing and packaging

## Learning Objectives (explicit)

By the end of Day 2, learners will be able to:

- Explain how `write_chapters()` fans out chapter generation concurrently.
- Trace chapter inputs from outline objects into chapter crew tasks.
- Tune chapter-writing prompts in YAML to improve structure and consistency.
- Validate generated chapter objects before aggregation.
- Identify and troubleshoot common async and output-quality issues.

## Target audience

- Learners who completed Day 1 or understand the project’s flow basics.
- Developers comfortable reading async Python patterns.
- Students interested in prompt+orchestration co-design for multi-agent systems.

## Prerequisites (detailed)

- Day 1 completed (or equivalent understanding of flow state + outline generation).
- Working environment with `crewai`, `crewai-tools`, `pydantic` installed.
- API keys configured for model provider and search tool usage.
- Ability to run `python main.py` from project root.

## Setup steps (full commands and checks)

1. Activate virtual environment:

```bash
source .venv/bin/activate
```

2. Confirm dependencies:

```bash
pip show crewai crewai-tools pydantic
```

3. Confirm environment variables:

```bash
env | grep -E "OPENAI_API_KEY|SERPER_API_KEY"
```

4. Ensure project root import path:

```bash
export PYTHONPATH="$PWD"
```

5. Run baseline flow once:

```bash
python main.py
```

6. Verify Day 2-ready baseline:
   - Outline prints successfully.
   - Chapter generation starts.
   - No schema/parsing exceptions in logs.

## Detailed Project Orientation (walkthrough)

Focus file order for Day 2:

- [main.py](main.py): inspect `write_chapters()` async fan-out and chapter collection.
- [types.py](types.py): re-check `Chapter` model expectations (`title`, `content`).
- [crews/write_book_chapter_crew/write_book_chapter_crew.py](crews/write_book_chapter_crew/write_book_chapter_crew.py): chapter crew wiring and `output_pydantic=Chapter`.
- [crews/write_book_chapter_crew/config/agents.yaml](crews/write_book_chapter_crew/config/agents.yaml): chapter researcher/writer role definitions.
- [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml): chapter research/write constraints and expected outputs.
- [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml): remind how outline quality affects chapter quality downstream.

Instructor note: show that Day 2 quality issues are often input-shaping issues from Day 1 outputs.

## Chapter Crew Deep Dive — `write_book_chapter_crew.py` + YAML configs

Open `crews/write_book_chapter_crew/write_book_chapter_crew.py` and cover:

1. Agent roles:
   - `researcher`: enriches chapter facts/context.
   - `writer`: synthesizes chapter markdown.
2. Task design:
   - `research_chapter` gathers support material.
   - `write_chapter` outputs structured `Chapter`.
3. Why `output_pydantic=Chapter` is critical for safe downstream aggregation.
4. Sequential process inside a single crew run, even while multiple chapter crew runs happen concurrently at flow level.

Then map this to YAML:

- `agents.yaml`: role/goal/backstory controls style and intent.
- `tasks.yaml`: chapter instructions, chapter length target, consistency requirements vs full outline.

## Async Flow Deep Dive — `write_chapters()` in `main.py`

Walk through `write_chapters()` step-by-step:

1. Internal async function `write_single_chapter(chapter_outline)`.
2. Per-chapter kickoff inputs:
   - `goal`
   - `topic`
   - `chapter_title`
   - `chapter_description`
   - serialized `book_outline`
3. Task scheduling loop with `asyncio.create_task(...)`.
4. Joining results via `await asyncio.gather(*tasks)`.
5. Persisting into `self.state.book`.

Teaching points:

- Concurrency in this flow is at chapter-level fan-out.
- Crew tasks inside each chapter run remain sequential.
- Error handling strategy can be per-task and aggregate-level.

## Live-coding block: Run and Harden Chapter Generation (step-by-step)

Step 0 — Baseline run and observe logs:

```bash
python main.py
```

Step 1 — Add structured debug logs in `write_chapters()` (temporary):

```python
print("Total outline chapters:", len(self.state.book_outline))
```

Step 2 — Before scheduling each task, print compact payload metadata:

```python
print({
    "chapter_title": chapter_outline.title,
    "desc_len": len(chapter_outline.description),
    "outline_size": len(self.state.book_outline)
})
```

Step 3 — Wrap chapter generation body with basic exception guard:

```python
try:
    output = WriteBookChapterCrew().crew().kickoff(inputs={...})
except Exception as e:
    print("Chapter generation failed:", str(e))
    return Chapter(title=chapter_outline.title, content=f"Generation failed: {e}")
```

Step 4 — Validate gathered results before extending state:

```python
for chapter in chapters:
    if not chapter.title or not chapter.content:
        print("Invalid chapter payload detected")
```

Step 5 — Re-run and verify:

```bash
python main.py
```

Step 6 — Remove noisy debug logs once behavior is stable.

## Speaker Notes & Teaching Tips

- Emphasize distinction between local sequential tasks and global concurrent chapter execution.
- Ask learners to predict which failures break one chapter vs entire run.
- Show how prompt constraints and typed outputs complement each other.
- Keep the first successful run small (2–3 chapters) if cost/time is a concern.

## Deep-dive: Concurrency, Cost, and Quality Trade-offs

Discuss practical trade-offs:

- More parallel chapters improve speed but increase simultaneous model/tool calls.
- Weak chapter prompts create inconsistency that appears as “random model behavior.”
- Quality control should occur at three levels:
  1. outline quality,
  2. chapter input payload quality,
  3. chapter output validation before aggregation.

Optional design idea to discuss (not mandatory implementation today):
- Add a simple semaphore to cap concurrent chapters for cost control.

## Troubleshooting Checklist (common errors and fixes)

- One chapter fails and stops entire gather
  - Use per-task exception handling so one failure returns fallback content.

- Empty or low-quality chapter output
  - Tighten `write_chapter` task constraints in YAML.
  - Ensure `chapter_description` is specific enough.

- Duplicate or overlapping chapter content
  - Add anti-overlap guidance in chapter task prompt.
  - Include clearer chapter boundaries from outline stage.

- Slow or rate-limited execution
  - Reduce number of chapters for classroom run.
  - Run chapters in smaller batches.

- Inconsistent markdown formatting
  - Add explicit markdown structure requirements in task prompt.

## Short Quiz (answers included)

Q1: Where is chapter concurrency implemented in this project?

- Answer: In `write_chapters()` inside `main.py`, using `asyncio.create_task` and `asyncio.gather`.

Q2: What schema validates chapter outputs?

- Answer: `Chapter` from `types.py` through `output_pydantic=Chapter`.

Q3: Are tasks inside `WriteBookChapterCrew` concurrent by default?

- Answer: No. The crew process is sequential; concurrency happens across chapter crew runs.

Q4: Which inputs most directly influence chapter relevance?

- Answer: `chapter_title`, `chapter_description`, `goal`, and full `book_outline` context.

Q5: Why validate outputs before extending `self.state.book`?

- Answer: To prevent malformed chapter data from breaking downstream assembly and save steps.

## Exercises / Try It Yourself (expanded — many step-by-step tasks)

Exercise 1 — Add chapter-level failure fallback (beginner/intermediate, 20 min)

- Goal: Ensure one failed chapter does not crash entire flow.
- Steps:
  1. Add `try/except` inside `write_single_chapter`.
  2. Return fallback `Chapter` object on exception.
  3. Confirm flow still completes with partial-success results.

Exercise 2 — Improve chapter coherence using YAML (intermediate, 20–30 min)

- Goal: Reduce chapter overlap and improve progression.
- Steps:
  1. Edit `write_chapter` task prompt in `crews/write_book_chapter_crew/config/tasks.yaml`.
  2. Add explicit “do not repeat content from previous chapters” instruction.
  3. Re-run and compare overlap qualitatively.

Exercise 3 — Add chapter quality validator (intermediate, 20 min)

- Goal: Enforce minimal chapter content criteria.
- Steps:
  1. Add a helper that checks title present and content length threshold.
  2. Log warnings for low-quality chapters.
  3. Keep list of invalid chapters for follow-up retry.

Exercise 4 — Concurrency cap experiment (advanced, 25–35 min)

- Goal: Compare full fan-out vs capped parallelism.
- Steps:
  1. Introduce `asyncio.Semaphore` around chapter kickoff.
  2. Run with cap of 2 and then 4.
  3. Compare runtime and output consistency.

Exercise 5 — Input payload introspection report (optional, 20 min)

- Goal: Build a compact per-chapter payload report for debugging.
- Steps:
  1. Capture title length, description length, and outline count.
  2. Print or save a small report before kickoff.
  3. Use report to explain quality differences between chapters.

## Expected outputs and validation

After Day 2 completion, learners should verify:

- Multiple chapters are generated from outline entries.
- `self.state.book` contains valid `Chapter` objects.
- Failures can be isolated without collapsing the entire run.
- Chapter prompts can be tuned to improve structure and reduce overlap.

## Example full code snippets (copyable)

Per-chapter guarded generation pattern:

```python
async def write_single_chapter(chapter_outline):
    try:
        output = (
            WriteBookChapterCrew()
            .crew()
            .kickoff(
                inputs={
                    "goal": self.state.goal,
                    "topic": self.state.topic,
                    "chapter_title": chapter_outline.title,
                    "chapter_description": chapter_outline.description,
                    "book_outline": [
                        item.model_dump_json() for item in self.state.book_outline
                    ],
                }
            )
        )
        return Chapter(title=output["title"], content=output["content"])
    except Exception as e:
        return Chapter(
            title=chapter_outline.title,
            content=f"Generation failed for this chapter: {e}",
        )
```

Simple chapter validation helper:

```python
def validate_chapter(chapter, min_chars=800):
    if not chapter.title.strip():
        return False, "Missing title"
    if len(chapter.content.strip()) < min_chars:
        return False, "Content too short"
    return True, "ok"
```

## Troubleshooting (expanded with examples)

- Error: `KeyError: 'content'` while parsing chapter output
  - Cause: model output not matching expected keys.
  - Fix: inspect raw output and strengthen task formatting instructions.

- Error: chapters generated but out-of-order presentation
  - Cause: concurrency completion order differs from outline order.
  - Fix: preserve original outline index and sort before final assembly.

- Error: repeated intro paragraphs across chapters
  - Cause: overly generic chapter prompts.
  - Fix: provide chapter-specific constraints and avoid repeating global intro.

- Error: high token/cost usage during classroom demo
  - Cause: full-length chapters for all outlines.
  - Fix: reduce chapter count or temporary word target during teaching run.

## Homework (before Day 3)

- Implement one quality validator and one failure fallback in chapter generation.
- Run two experiments with different chapter prompt constraints and compare output quality.
- Prepare one proposal for improving `join_and_save_chapter()` formatting for publishing.

## Advanced topics to mention (briefly, for curious learners)

- Partial retries for failed chapters instead of full-flow reruns.
- Deterministic chapter ordering in concurrent pipelines.
- Automated chapter quality scoring (style, coverage, redundancy).

## Glossary

- Fan-out: launching multiple chapter generation tasks from one outline list.
- Gather: collecting multiple async task results with `asyncio.gather`.
- Fallback chapter: safe placeholder output returned when chapter generation fails.
- Coherence: how well a chapter aligns with book goal and neighboring chapters.

## Additional resources

- Python asyncio tasks: https://docs.python.org/3/library/asyncio-task.html
- CrewAI docs: https://docs.crewai.com
- Prompt design basics: https://platform.openai.com/docs/guides/prompt-engineering

## Full checklist for the instructor

1. Reconfirm environment variables and dependency health.
2. Walk through chapter crew Python + YAML configuration.
3. Explain and demonstrate async fan-out in `write_chapters()`.
4. Run at least one guarded chapter generation demo.
5. Execute quiz and one hands-on exercise.
6. Assign Day 2 homework and preview Day 3 output packaging.

---

Files referenced in this lesson:
- [main.py](main.py)
- [types.py](types.py)
- [crews/write_book_chapter_crew/write_book_chapter_crew.py](crews/write_book_chapter_crew/write_book_chapter_crew.py)
- [crews/write_book_chapter_crew/config/agents.yaml](crews/write_book_chapter_crew/config/agents.yaml)
- [crews/write_book_chapter_crew/config/tasks.yaml](crews/write_book_chapter_crew/config/tasks.yaml)
- [crews/outline_book_crew/config/tasks.yaml](crews/outline_book_crew/config/tasks.yaml)
