"""Minimal CLI skeleton.

Example:
  python -m company_analysis generate AAPL --industry software-platform --output reports/
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .pipeline import generate_report_bundle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="company_analysis")
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="Generate report bundle for a ticker")
    gen.add_argument("ticker")
    gen.add_argument("--industry", default="auto", help="metric pack name, e.g. saas-cloud")
    gen.add_argument("--output", default="reports")
    gen.add_argument("--allow-placeholder", action="store_true", help="allow skeleton output with missing live data")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "generate":
        output_dir = Path(args.output)
        bundle = generate_report_bundle(
            ticker=args.ticker.upper(),
            industry=args.industry,
            output_dir=output_dir,
            allow_placeholder=args.allow_placeholder,
        )
        print(json.dumps({"date": str(date.today()), "outputs": bundle}, indent=2))
        return 0
    return 2
