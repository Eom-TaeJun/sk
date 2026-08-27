from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import run_h1_backtest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the deterministic H1 demand-signal historical backtest"
    )
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--config", default="data/backtest/config.json")
    parser.add_argument("--sources", default="data/backtest/source_registry.jsonl")
    parser.add_argument("--events", default="data/backtest/events.jsonl")
    parser.add_argument("--cases", default="data/backtest/cases.json")
    args = parser.parse_args()
    root = Path(args.workspace).resolve()

    def resolved(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else root / path

    result = run_h1_backtest(
        root,
        resolved(args.config),
        resolved(args.sources),
        resolved(args.events),
        resolved(args.cases),
    )
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
