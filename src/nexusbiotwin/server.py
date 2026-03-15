from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .compiler import compile_mission, render_report, write_run
from .models import Mission

STATIC_DIR = Path(__file__).parent / "static"
RUNS_DIR = Path("runs") / "gui"

app = FastAPI(title="NexusBioTwin Studio")

# Mount static files (CSS, JS) except index.html which we serve on root
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not built or static files missing.")
    return FileResponse(index_path)


def _archive_dir_for(mission_id: str) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    safe_id = re.sub(r"[^A-Za-z0-9._-]+", "_", mission_id).strip("._") or "mission"
    return RUNS_DIR / f"{stamp}_{safe_id}"


def _runs_root() -> Path:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    return RUNS_DIR.resolve()


def _resolve_run_dir(run_id: str) -> Path:
    safe_id = run_id.strip()
    if not safe_id:
        raise HTTPException(status_code=400, detail="run id is required")

    root = _runs_root()
    candidate = (root / safe_id).resolve()
    if candidate.parent != root or not candidate.is_dir():
        raise HTTPException(status_code=404, detail="run not found")
    return candidate


def _read_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _run_summary(run_dir: Path) -> dict[str, Any] | None:
    manifest = _read_json(run_dir / "manifest.json")
    plan = _read_json(run_dir / "plan.json")
    if not isinstance(plan, dict):
        return None

    manifest = manifest if isinstance(manifest, dict) else {}
    summary = manifest.get("summary")
    if not isinstance(summary, dict):
        summary = plan.get("summary", {})

    warnings = plan.get("warnings", [])
    active_innovations = plan.get("active_innovations", manifest.get("active_innovations", []))
    generated_at = manifest.get("generated_at")
    archive_root = _runs_root()

    return {
        "run_id": run_dir.name,
        "archive_dir": str(run_dir.relative_to(archive_root)),
        "generated_at": generated_at,
        "mission_id": plan.get("mission_id") or manifest.get("mission_id") or run_dir.name,
        "mission_name": plan.get("mission_name") or manifest.get("mission_name") or plan.get("mission_id") or run_dir.name,
        "risk_tier": plan.get("risk_tier") or manifest.get("risk_tier") or "unknown",
        "summary": summary,
        "warning_count": len(warnings) if isinstance(warnings, list) else 0,
        "innovation_count": len(active_innovations) if isinstance(active_innovations, list) else 0,
    }


@app.post("/api/compile")
async def api_compile(mission_payload: dict):
    try:
        mission = Mission(**mission_payload)
        plan = compile_mission(mission)
        report = render_report(mission, plan)
        archive_dir = write_run(_archive_dir_for(mission.mission_id), mission, plan)
        manifest = _read_json(archive_dir / "manifest.json")
        return {
            "status": "success",
            "plan": plan,
            "report": report,
            "manifest": manifest,
            "mission": asdict(mission),
            "archive_dir": str(archive_dir),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/runs")
async def api_runs(limit: int = 30):
    clamped_limit = max(1, min(limit, 200))
    runs: list[dict[str, Any]] = []
    for run_dir in sorted(_runs_root().iterdir(), key=lambda item: item.name, reverse=True):
        if not run_dir.is_dir():
            continue
        summary = _run_summary(run_dir)
        if summary is None:
            continue
        runs.append(summary)
        if len(runs) >= clamped_limit:
            break
    return {"runs": runs}


@app.get("/api/runs/{run_id}")
async def api_run_detail(run_id: str):
    run_dir = _resolve_run_dir(run_id)
    plan = _read_json(run_dir / "plan.json")
    report = _read_text(run_dir / "report.md")
    if not isinstance(plan, dict) or report is None:
        raise HTTPException(status_code=404, detail="run artifacts are incomplete")

    return {
        "run_id": run_dir.name,
        "archive_dir": str(run_dir),
        "manifest": _read_json(run_dir / "manifest.json"),
        "mission": _read_json(run_dir / "mission.json"),
        "plan": plan,
        "report": report,
        "files": sorted(path.name for path in run_dir.iterdir() if path.is_file()),
    }
