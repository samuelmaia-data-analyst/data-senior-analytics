# Data Lineage and Reproducibility

## Purpose
This document describes how data artifacts are tracked to ensure reproducibility and auditability.

## Manifest Strategy
- Manifest file: `docs/data_manifest.json`
- Generation script: `scripts/generate_data_manifest.py`
- Scope: `data/sample/*` and `data/raw/*` tabular files
- Tracked fields per file:
  - Relative path
  - File size in bytes
  - Last modified timestamp (UTC)
  - SHA-256 checksum
  - Optional shape (`rows`, `columns`) for CSV/XLSX

## Operational Flow
1. Update or add dataset files.
2. Regenerate manifest:
   - `python scripts/generate_data_manifest.py`
3. Validate in CI/local:
   - `python scripts/generate_data_manifest.py --check`

## Why This Matters
- Detects unintended data drift in versioned datasets.
- Improves confidence in reproducing analytical outputs.
- Provides clear lineage evidence for reviewers and technical leads.
