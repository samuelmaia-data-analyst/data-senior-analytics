"""Shared analytics utilities for the dashboard."""

from __future__ import annotations

import numpy as np
import pandas as pd


def detect_column_types(df: pd.DataFrame) -> dict[str, list[str]]:
    """Detect and categorize columns by semantic type."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    raw_categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    for col in raw_categorical_cols:
        if col in date_cols:
            continue
        non_null = df[col].dropna()
        if non_null.empty:
            continue
        sample_size = min(len(non_null), 200)
        sample = (
            non_null.sample(n=sample_size, random_state=42)
            if len(non_null) > sample_size
            else non_null
        )
        parsed = pd.to_datetime(sample, errors="coerce")
        if parsed.notna().mean() >= 0.8 and col not in date_cols:
            date_cols.append(col)

    categorical_cols = [c for c in raw_categorical_cols if c not in date_cols]

    id_cols = []
    for col in numeric_cols:
        if df[col].nunique() > len(df) * 0.9:
            id_cols.append(col)

    bool_cols = df.select_dtypes(include=["bool"]).columns.tolist()

    return {
        "numeric": [c for c in numeric_cols if c not in id_cols],
        "categorical": categorical_cols,
        "date": date_cols,
        "id": id_cols,
        "boolean": bool_cols,
        "all_numeric": numeric_cols,
    }


def get_basic_stats(df: pd.DataFrame, col: str) -> dict[str, float | int | None]:
    """Return descriptive statistics for a numeric column."""
    stats_dict: dict[str, float | int | None] = {}
    if col in df.select_dtypes(include=[np.number]).columns:
        stats_dict["Média"] = df[col].mean()
        stats_dict["Mediana"] = df[col].median()
        stats_dict["Moda"] = df[col].mode()[0] if not df[col].mode().empty else None
        stats_dict["Desvio Padrão"] = df[col].std()
        stats_dict["Variância"] = df[col].var()
        stats_dict["Mínimo"] = df[col].min()
        stats_dict["Máximo"] = df[col].max()
        stats_dict["Q1"] = df[col].quantile(0.25)
        stats_dict["Q3"] = df[col].quantile(0.75)
        stats_dict["IQR"] = stats_dict["Q3"] - stats_dict["Q1"]
        stats_dict["Assimetria"] = df[col].skew()
        stats_dict["Curtose"] = df[col].kurtosis()
    return stats_dict


def interpret_correlation(corr: float) -> tuple[str, str]:
    """Interpret correlation strength."""
    if abs(corr) > 0.9:
        return "Muito Forte", "🔥"
    if abs(corr) > 0.7:
        return "Forte", "💪"
    if abs(corr) > 0.5:
        return "Moderada", "👍"
    if abs(corr) > 0.3:
        return "Fraca", "👎"
    return "Muito Fraca", "❌"


def build_data_quality_summary(df: pd.DataFrame) -> dict[str, float | int | str]:
    """Build an executive-ready summary of dataset quality."""
    rows, columns = df.shape
    total_cells = max(1, rows * columns)
    missing_count = int(df.isna().sum().sum())
    duplicate_count = int(df.duplicated().sum())
    numeric_count = int(df.select_dtypes(include=[np.number]).shape[1])
    categorical_count = int(df.select_dtypes(include=["object", "category"]).shape[1])
    datetime_count = int(df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).shape[1])
    memory_mb = float(df.memory_usage(deep=True).sum() / (1024 * 1024))

    missing_pct = float((missing_count / total_cells) * 100)
    duplicate_pct = float((duplicate_count / max(1, rows)) * 100)
    completeness_pct = float(100 - missing_pct)

    score = max(
        0.0,
        min(
            100.0,
            100.0
            - (missing_pct * 2.2)
            - (duplicate_pct * 1.3)
            - (8.0 if numeric_count == 0 else 0.0)
            - (5.0 if rows < 20 else 0.0),
        ),
    )

    if score >= 90:
        status = "Excellent"
    elif score >= 75:
        status = "Good"
    elif score >= 60:
        status = "Attention"
    else:
        status = "Critical"

    return {
        "rows": rows,
        "columns": columns,
        "missing_count": missing_count,
        "missing_pct": missing_pct,
        "duplicate_count": duplicate_count,
        "duplicate_pct": duplicate_pct,
        "numeric_columns": numeric_count,
        "categorical_columns": categorical_count,
        "datetime_columns": datetime_count,
        "memory_mb": memory_mb,
        "completeness_pct": completeness_pct,
        "quality_score": round(score, 2),
        "status": status,
    }


def build_priority_actions(summary: dict[str, float | int | str]) -> list[str]:
    """Translate quality metrics into concrete next actions."""
    actions: list[str] = []

    if float(summary["missing_pct"]) > 5:
        actions.append("Prioritize null handling before sharing executive insights.")
    if float(summary["duplicate_pct"]) > 1:
        actions.append("Review business keys and deduplication to avoid double counting.")
    if int(summary["numeric_columns"]) == 0:
        actions.append("Add numeric measures to unlock KPI, correlation, and trend analysis.")
    if int(summary["rows"]) < 20:
        actions.append("Increase sample size before making high-confidence decisions.")
    if not actions:
        actions.append("Dataset is ready for executive exploration and analytical persistence.")

    return actions


def summarize_transformation_log(log: list[dict]) -> list[str]:
    """Convert the transformation log into UI-ready statements."""
    summary: list[str] = []
    for item in log:
        operation = item.get("operation", "unknown")
        details = item.get("details", {})

        if operation == "clean_column_names":
            original = details.get("original", [])
            new = details.get("new", [])
            renamed = sum(
                1 for old, new_name in zip(original, new, strict=False) if old != new_name
            )
            summary.append(f"Column standardization applied to {renamed} fields.")
        elif operation == "convert_dtypes":
            summary.append("Automatic dtype inference executed for object columns.")
        elif operation == "handle_missing_values":
            before = details.get("missing_before", 0)
            after = details.get("missing_after", 0)
            summary.append(f"Missing values reduced from {before} to {after}.")
        elif operation == "remove_duplicates":
            removed = details.get("removed", 0)
            summary.append(f"Duplicate removal eliminated {removed} rows.")
        elif operation == "create_features":
            summary.append("Feature generation step executed.")

    return summary
