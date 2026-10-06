from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
H1_WORKSPACE_INPUTS = (
    "data/h1",
    "data/raw/sources",
    "application_evidence/capability_evidence_ledger.json",
    "docs/reviews/h1_gate6_corpus_readiness.md",
    "src/measurement/corpus.py",
    "src/measurement/validation.py",
    "tests/test_h1_full_corpus.py",
)


def _input_hashes() -> dict[str, str]:
    hashes = {}
    for relative in H1_WORKSPACE_INPUTS:
        source = REPO_ROOT / relative
        paths = source.rglob("*") if source.is_dir() else (source,)
        for path in paths:
            if path.is_file():
                hashes[path.relative_to(REPO_ROOT).as_posix()] = hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
    return hashes


def isolated_h1_workspace(test_case: type[unittest.TestCase]) -> Path:
    before = _input_hashes()
    tempdir = tempfile.TemporaryDirectory(prefix="h1-test-")
    test_case.addClassCleanup(tempdir.cleanup)
    workspace = Path(tempdir.name)
    for relative in H1_WORKSPACE_INPUTS:
        source = REPO_ROOT / relative
        target = workspace / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)

    def assert_original_inputs_unchanged() -> None:
        after = _input_hashes()
        if before != after:
            changed = sorted(
                path for path in set(before) | set(after)
                if before.get(path) != after.get(path)
            )
            raise AssertionError(f"tests changed repository input bytes: {changed}")

    test_case.addClassCleanup(assert_original_inputs_unchanged)
    return workspace
