"""Generate or validate a versioned data manifest for reproducibility."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

DEFAULT_TARGET = Path("docs/data_manifest.json")
DATA_GLOBS = (
    "data/sample/*.csv",
    "data/raw/*.csv",
    "data/raw/*.xlsx",
    "data/raw/*.xls",
)


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    if path.suffix.lower() == ".csv":
        # Normalize newlines to avoid cross-platform checksum drift.
        content = path.read_bytes().replace(b"\r\n", b"\n")
        hasher.update(content)
        return hasher.hexdigest()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def get_shape(path: Path) -> dict[str, int] | None:
    try:
        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
            return {"rows": int(df.shape[0]), "columns": int(df.shape[1])}
        if path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(path)
            return {"rows": int(df.shape[0]), "columns": int(df.shape[1])}
    except Exception:  # noqa: BLE001
        return None
    return None


def build_manifest(root: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for pattern in DATA_GLOBS:
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            stat = path.stat()
            entry: dict[str, object] = {
                "path": rel,
                "size_bytes": int(stat.st_size),
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=UTC).isoformat(),
                "sha256": sha256_file(path),
            }
            shape = get_shape(path)
            if shape:
                entry["shape"] = shape
            files.append(entry)

    return {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_patterns": list(DATA_GLOBS),
        "files": files,
    }


def normalize_for_check(manifest: dict[str, object]) -> dict[str, object]:
    normalized = dict(manifest)
    normalized["generated_at_utc"] = "IGNORED"
    normalized_files = []
    for entry in normalized.get("files", []):
        if not isinstance(entry, dict):
            continue
        normalized_files.append(
            {
                "path": entry.get("path"),
                "sha256": entry.get("sha256"),
                "shape": entry.get("shape"),
            }
        )
    normalized["files"] = normalized_files
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--check", action="store_true", help="Fail if existing manifest differs")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = build_manifest(root)
    target = root / args.output

    if args.check:
        if not target.exists():
            print(f"Manifest check failed: missing file {args.output}")
            return 1
        existing = json.loads(target.read_text(encoding="utf-8"))
        if normalize_for_check(existing) != normalize_for_check(manifest):
            print("Manifest check failed: docs/data_manifest.json is outdated.")
            print("Run: python scripts/generate_data_manifest.py")
            return 1
        print("Data manifest check passed.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Data manifest generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
