"""Fail CI when likely secrets are committed."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

PATTERNS = {
    "AWS Access Key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Private Key Block": re.compile(r"-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----"),
    "GitHub Token": re.compile(r"\bghp_[A-Za-z0-9]{36}\b"),
    "Slack Token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
}

IGNORED_FILES = {
    ".env.example",
    ".streamlit/secrets.example.toml",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".sql",
    ".ini",
    ".cfg",
    ".env",
}


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], text=True)
    return [Path(line.strip()) for line in out.splitlines() if line.strip()]


def should_scan(path: Path) -> bool:
    rel = path.as_posix()
    if rel in IGNORED_FILES:
        return False
    if path.suffix and path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False
    return True


def scan_file(path: Path) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    findings: list[str] = []
    for label, pattern in PATTERNS.items():
        if pattern.search(content):
            findings.append(label)
    return findings


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    failures: list[str] = []
    for rel_path in tracked_files():
        if not should_scan(rel_path):
            continue
        full = repo_root / rel_path
        if not full.exists() or not full.is_file():
            continue
        hits = scan_file(full)
        for hit in hits:
            failures.append(f"{rel_path.as_posix()}: {hit}")

    if failures:
        print("Secret scan failed. Potential secrets found:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Secret scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
