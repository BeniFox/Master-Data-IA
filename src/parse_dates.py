
import pandas as pd


def parse_dates(values, dayfirst=True):
    values = pd.Series(values).copy()
    parsed = pd.to_datetime(values, errors="coerce", dayfirst=dayfirst)

    total = len(values)
    converted = int(parsed.notna().sum())
    failed = int(parsed.isna().sum())

    report = {
        "total": total,
        "converties": converted,
        "echecs": failed,
        "taux_conversion_pct": round(converted / total * 100, 2) if total else 0.0,
    }

    return parsed, report
