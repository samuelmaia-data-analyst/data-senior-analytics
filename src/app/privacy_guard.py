"""Privacy and governance helpers for LGPD-aware analytics workflows."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

POLICY_PATH = Path(__file__).resolve().parents[2] / "config" / "privacy_policy.json"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CPF_RE = re.compile(r"^\d{11}$")
PHONE_RE = re.compile(r"^\+?\d{10,13}$")


@lru_cache(maxsize=1)
def load_privacy_policy() -> dict[str, Any]:
    with POLICY_PATH.open(encoding="utf-8") as policy_file:
        return json.load(policy_file)


def _looks_like_email(series: pd.Series, min_ratio: float) -> bool:
    non_null = series.dropna().astype(str).str.strip()
    if non_null.empty:
        return False
    sample = non_null.head(100)
    ratio = float(sample.apply(lambda value: bool(EMAIL_RE.match(value))).mean())
    return ratio >= min_ratio


def _looks_like_cpf(series: pd.Series, min_ratio: float) -> bool:
    non_null = series.dropna().astype(str).str.strip()
    if non_null.empty:
        return False
    sample = non_null.head(100)
    ratio = float(sample.apply(lambda value: bool(CPF_RE.match(re.sub(r"\D", "", value)))).mean())
    return ratio >= min_ratio


def _looks_like_phone(series: pd.Series, min_ratio: float) -> bool:
    non_null = series.dropna().astype(str).str.strip()
    if non_null.empty:
        return False
    sample = non_null.head(100)
    ratio = float(sample.apply(lambda value: bool(PHONE_RE.match(re.sub(r"\D", "", value)))).mean())
    return ratio >= min_ratio


def detect_sensitive_columns(df: pd.DataFrame) -> dict[str, list[str]]:
    """Classify columns that should trigger privacy controls."""
    policy = load_privacy_policy()
    direct_patterns = tuple(policy["direct_identifier_patterns"])
    sensitive_patterns = tuple(policy["sensitive_patterns"])
    quasi_patterns = tuple(policy["quasi_identifier_patterns"])
    content_rules = policy["content_rules"]

    direct_identifiers: list[str] = []
    sensitive_columns: list[str] = []
    quasi_identifiers: list[str] = []

    for column in df.columns:
        normalized = str(column).lower()
        series = df[column]

        if any(pattern in normalized for pattern in sensitive_patterns):
            sensitive_columns.append(column)
            continue

        is_direct = any(pattern in normalized for pattern in direct_patterns)
        is_quasi = any(pattern in normalized for pattern in quasi_patterns)

        if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
            if _looks_like_email(series, float(content_rules["email_min_ratio"])):
                is_direct = True
            if _looks_like_cpf(series, float(content_rules["cpf_min_ratio"])):
                is_direct = True
            if _looks_like_phone(series, float(content_rules["phone_min_ratio"])):
                is_direct = True

        if is_direct:
            direct_identifiers.append(column)
        elif is_quasi:
            quasi_identifiers.append(column)

    personal_columns = sorted(set(direct_identifiers + quasi_identifiers + sensitive_columns))
    return {
        "personal_columns": personal_columns,
        "direct_identifiers": sorted(set(direct_identifiers)),
        "sensitive_columns": sorted(set(sensitive_columns)),
        "quasi_identifiers": sorted(set(quasi_identifiers)),
    }


def _mask_value(value: Any) -> Any:
    if pd.isna(value):
        return value
    text = str(value)
    if len(text) <= 4:
        return "*" * len(text)
    visible_suffix = text[-2:]
    return f"{'*' * max(2, len(text) - 2)}{visible_suffix}"


def mask_sensitive_dataframe(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    masked = df.copy()
    for column in columns:
        if column in masked.columns:
            masked[column] = masked[column].apply(_mask_value)
    return masked


def build_privacy_snapshot(df: pd.DataFrame) -> dict[str, Any]:
    """Build LGPD-oriented privacy controls for UI and persistence decisions."""
    classifications = detect_sensitive_columns(df)
    direct_identifiers = classifications["direct_identifiers"]
    sensitive_columns = classifications["sensitive_columns"]
    quasi_identifiers = classifications["quasi_identifiers"]
    personal_columns = classifications["personal_columns"]

    if sensitive_columns:
        risk_level = "High"
    elif direct_identifiers:
        risk_level = "Medium"
    elif quasi_identifiers:
        risk_level = "Low"
    else:
        risk_level = "Minimal"

    masked_preview = mask_sensitive_dataframe(df.head(200), personal_columns)
    safe_persistence_default = bool(personal_columns)

    controls = []
    if personal_columns:
        controls.append("Mask previews and avoid exposing direct identifiers in the interface.")
        controls.append(
            "Persist a masked copy by default unless there is a documented lawful basis."
        )
    if sensitive_columns:
        controls.append(
            "Sensitive personal data requires stricter handling and explicit review before storage."
        )
    if not controls:
        controls.append("No obvious personal data indicators were detected in the current dataset.")

    return {
        "risk_level": risk_level,
        "personal_columns": personal_columns,
        "direct_identifiers": direct_identifiers,
        "sensitive_columns": sensitive_columns,
        "quasi_identifiers": quasi_identifiers,
        "personal_data_detected": bool(personal_columns),
        "sensitive_data_detected": bool(sensitive_columns),
        "safe_persistence_default": safe_persistence_default,
        "controls": controls,
        "masked_preview": masked_preview,
    }


@dataclass
class PrivacyArtifacts:
    privacy_snapshot: dict[str, Any]
    masked_curated_df: pd.DataFrame
