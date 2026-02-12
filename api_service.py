from datetime import datetime, timezone
import os
import subprocess
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class GenerateBookRequest(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    goal: Optional[str] = None


app = FastAPI(title="CrewAI Optional API Adapter", version="0.1.0")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "cli-primary",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/generate-book")
def generate_book(_: GenerateBookRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
    if not os.getenv("SERPER_API_KEY"):
        raise HTTPException(status_code=500, detail="SERPER_API_KEY is not set")

    try:
        result = subprocess.run(
            ["python", "main.py"],
            check=True,
            capture_output=True,
            text=True,
            timeout=1800,
        )
    except subprocess.TimeoutExpired as error:
        raise HTTPException(status_code=504, detail="Generation timed out") from error
    except subprocess.CalledProcessError as error:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "CLI generation failed",
                "stdout": error.stdout[-4000:] if error.stdout else "",
                "stderr": error.stderr[-4000:] if error.stderr else "",
            },
        ) from error

    return {
        "status": "completed",
        "mode": "cli-flow-invoked",
        "stdout_tail": result.stdout[-2000:] if result.stdout else "",
    }
