from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class DuplicateConflict(ValueError):
    """Same identifier was seen with different immutable content."""


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_digest(data: Any) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest().upper()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    path.write_text(rendered, encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def put_jsonl(
    path: Path,
    record: dict[str, Any],
    id_field: str,
    immutable: bool = False,
) -> bool:
    records = load_jsonl(path)
    found = False
    changed = False
    output: list[dict[str, Any]] = []
    for existing in records:
        if existing[id_field] != record[id_field]:
            output.append(existing)
            continue
        found = True
        if canonical_json(existing) != canonical_json(record):
            if immutable:
                raise DuplicateConflict(f"{id_field} {record[id_field]} has conflicting content")
            output.append(record)
            changed = True
        else:
            output.append(existing)
    if not found:
        output.append(record)
        changed = True
    output.sort(key=lambda item: item[id_field])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in output:
            handle.write(canonical_json(item) + "\n")
    return changed


class SourceRegistry:
    def __init__(self, path: Path):
        self.path = path

    def register(self, source: dict[str, Any]) -> bool:
        return put_jsonl(self.path, source, "source_id", immutable=True)

    def as_map(self) -> dict[str, dict[str, Any]]:
        return {item["source_id"]: item for item in load_jsonl(self.path)}


class EvidenceRegistry:
    def __init__(self, path: Path):
        self.path = path

    def put(self, evidence: dict[str, Any]) -> bool:
        return put_jsonl(self.path, evidence, "evidence_id", immutable=False)

    def all(self) -> list[dict[str, Any]]:
        return load_jsonl(self.path)

    def as_map(self) -> dict[str, dict[str, Any]]:
        return {item["evidence_id"]: item for item in self.all()}


class ReviewRegistry:
    def __init__(self, path: Path):
        self.path = path

    def register(self, review: dict[str, Any]) -> bool:
        return put_jsonl(self.path, review, "review_id", immutable=True)

    def all(self) -> list[dict[str, Any]]:
        return load_jsonl(self.path)

    def for_run(self, run_id: str) -> list[dict[str, Any]]:
        return [item for item in self.all() if item["run_id"] == run_id]
