import pandas as pd

from src.app.privacy_guard import build_privacy_snapshot, detect_sensitive_columns


def test_detect_sensitive_columns_flags_direct_and_sensitive_fields():
    df = pd.DataFrame(
        {
            "nome_cliente": ["Ana", "Bruno"],
            "email": ["ana@example.com", "bruno@example.com"],
            "cpf": ["12345678901", "98765432100"],
            "diagnostico": ["A", "B"],
            "valor_total": [10.0, 20.0],
        }
    )

    result = detect_sensitive_columns(df)

    assert "email" in result["direct_identifiers"]
    assert "cpf" in result["direct_identifiers"]
    assert "diagnostico" in result["sensitive_columns"]
    assert "nome_cliente" in result["personal_columns"]


def test_build_privacy_snapshot_masks_detected_personal_columns():
    df = pd.DataFrame(
        {
            "email": ["ana@example.com"],
            "cliente_id": [101],
            "valor_total": [50.0],
        }
    )

    snapshot = build_privacy_snapshot(df)

    assert snapshot["personal_data_detected"] is True
    assert snapshot["risk_level"] == "Medium"
    assert snapshot["safe_persistence_default"] is True
    assert snapshot["masked_preview"].iloc[0]["email"] != "ana@example.com"
