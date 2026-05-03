"""
Module 04 — Packaging Your Agent as a CLI Tool
===============================================
A research agent is only useful if teammates can run it easily.
This module wraps the multi-agent pipeline from module_03 behind
a proper CLI using Python's standard argparse library.

Usage examples:
  python module_04_cli.py --goal "Explain RAG pipelines"
  python module_04_cli.py --goal "Compare GPT-4 and Claude 3" --output report.md
  python module_04_cli.py --interactive
"""

import argparse
import sys
from pathlib import Path

# Import our pipeline (adjust if running from a different working directory)
try:
    from module_03_multi_agent import MultiAgentPipeline
except ModuleNotFoundError:
    # Allow running standalone
    class MultiAgentPipeline:  # type: ignore
        def run(self, goal: str):
            from types import SimpleNamespace
            return SimpleNamespace(goal=goal, content=f"[Stub report for: {goal}]")


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def write_output(content: str, path: str | None) -> None:
    if path:
        Path(path).write_text(content, encoding="utf-8")
        print(f"Report written to {path}")
    else:
        print("\n" + "=" * 60)
        print(content)
        print("=" * 60)


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def run_single(args) -> None:
    pipeline = MultiAgentPipeline()
    report = pipeline.run(args.goal)
    write_output(report.content, args.output)


def run_interactive(args) -> None:
    pipeline = MultiAgentPipeline()
    print("Interactive research agent. Type 'quit' to exit.")
    while True:
        try:
            goal = input("\nResearch goal> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break
        if goal.lower() in {"quit", "exit", "q"}:
            print("Goodbye.")
            break
        if not goal:
            continue
        report = pipeline.run(goal)
        write_output(report.content, None)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-agent",
        description="Multi-agent research pipeline: Planner → Researcher → Writer",
    )
    sub = parser.add_subparsers(dest="command")

    # Single-shot mode
    run_cmd = sub.add_parser("run", help="Run a single research goal")
    run_cmd.add_argument("goal", help="The research goal or question")
    run_cmd.add_argument("--output", "-o", help="Save report to this file (Markdown)")

    # Interactive mode
    sub.add_parser("interactive", help="Start an interactive session")

    # Backwards-compat: no subcommand → use --goal flag
    parser.add_argument("--goal", help="Research goal (single-shot, no subcommand needed)")
    parser.add_argument("--output", "-o", help="Save report to file")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        run_single(args)
    elif args.command == "interactive":
        run_interactive(args)
    elif args.interactive:
        run_interactive(args)
    elif args.goal:
        run_single(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
