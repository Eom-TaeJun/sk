"""Offline probes accompanying the dated code review, not a quality gate.

Run from any directory: python -B docs/reviews/2026-10-06/reproduce_findings.py
Only synthetic fixtures and temporary workspace copies are modified. Output is
JSON on stdout; an exit code of zero means probes ran, not that code is correct.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

import scripts.collect_customer_commitment as collector
from src.pipeline import run_vertical_slice
from tests.test_customer_commitment_collection import SYNTHETIC_DOCUMENT, SYNTHETIC_INDEX
from tests.test_vertical_slice import VerticalSliceTest


def main() -> None:
    temporary_root = (REPO / "work" / "code_review_20261006").resolve()
    if not temporary_root.is_relative_to(REPO.resolve()):
        raise ValueError("temporary workspace escapes the repository")
    temporary_root.mkdir(parents=True, exist_ok=True)
    observations = []
    with patch.object(tempfile, "tempdir", str(temporary_root)):
        bad_index = SYNTHETIC_INDEX.replace(
            b"2025-09-25 09:00:25", b"2025-99-99 99:99:99"
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "candidate"
            collector.capture(
                output, {"document": SYNTHETIC_DOCUMENT, "index": bad_index},
                mode="offline_import", allow_synthetic=True,
                timestamp="not-an-ISO-date",
            )
            record = json.loads((output / "record.json").read_text(encoding="utf-8"))
            observations.append({
                "probe": "invalid timestamps",
                "accepted_at_source": record["accepted_at_source"],
                "retrieved_at_utc": record["retrieved_at_utc"],
                "verify": collector.verify_capture(output),
            })

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "candidate"
            documents = {"document": SYNTHETIC_DOCUMENT, "index": SYNTHETIC_INDEX}
            collector.capture(
                output, documents, mode="offline_import", allow_synthetic=True,
                timestamp="2026-10-03T01:00:00Z",
            )
            revision = dict(documents, document=SYNTHETIC_DOCUMENT + b"\n<!-- revision -->\n")
            original_write_current = collector.write_current

            def interrupted_ledger(path, raw):
                if path.name == "acquisition.json":
                    raise OSError("SIMULATED_DISK_WRITE_FAILURE")
                return original_write_current(path, raw)

            with patch.object(collector, "write_current", side_effect=interrupted_ledger):
                try:
                    collector.capture(
                        output, revision, mode="offline_import", allow_synthetic=True,
                        timestamp="2026-10-04T01:00:00Z",
                    )
                except OSError:
                    pass
            for action in ("verify", "retry"):
                try:
                    actual = (
                        collector.verify_capture(output) if action == "verify"
                        else collector.capture(
                            output, revision, mode="offline_import", allow_synthetic=True,
                            timestamp="2026-10-04T01:00:00Z",
                        )
                    )
                except collector.CaptureError as error:
                    actual = {"exception": type(error).__name__, "message": str(error)}
                observations.append({
                    "probe": "interrupted capture publication",
                    "action": action, "actual": actual,
                })

        case = VerticalSliceTest()
        case.setUp()
        try:
            first = run_vertical_slice(case.workspace, case.baseline_path)
            archive = case.workspace / "data/raw/sources/SRC-SKH-20250319-HBM4-SAMPLE.md"
            archive.write_bytes(b"CHANGED SOURCE CONTENT AFTER FIRST RUN")
            replay = run_vertical_slice(case.workspace, case.baseline_path)
            observations.append({
                "probe": "cache after source change",
                "returns_prior_result": replay == first,
                "review_status": replay["memo"]["review_status"],
                "trace_hash": replay["trace_hash"],
            })
        finally:
            case.tearDown()

    print(json.dumps(observations, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
