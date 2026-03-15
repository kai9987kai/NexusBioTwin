from __future__ import annotations

import argparse
from pathlib import Path

from .compiler import compile_mission, load_mission, write_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexusbiotwin",
        description="Compile a mission JSON file into a NexusBioTwin planning run.",
    )
    parser.add_argument("mission", type=Path, nargs="?", help="Path to the mission JSON file.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/latest"),
        help="Directory where the run archive will be written.",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Launch the local GUI server instead of running a CLI compilation.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the GUI server on (default: 8000).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.serve:
        import uvicorn
        from .server import app
        print(f"Starting NexusBioTwin Operator Studio on port {args.port}...")
        uvicorn.run(app, host="127.0.0.1", port=args.port)
        return 0

    if not args.mission:
        parser.error("The 'mission' argument is required unless running with --serve.")

    mission = load_mission(args.mission)
    plan = compile_mission(mission)
    output_dir = write_run(args.output, mission, plan)

    print(f"compiled mission {mission.mission_id}")
    print(f"risk tier: {plan['risk_tier']}")
    print(f"run written to: {output_dir}")
    return 0
