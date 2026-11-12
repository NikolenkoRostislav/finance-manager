import json
import shutil
from pathlib import Path

import pytest

from budget_tracker.analytics import generate_analytics
from budget_tracker.categorizer import categorize
from budget_tracker.cleaning import clean
from budget_tracker.config import Config
from budget_tracker.loaders import load_data

ROOT = Path(__file__).resolve().parent.parent
TINY_EXPORTS = ROOT / "tests_data" / "tiny_exports"
EXPECTED = json.loads((ROOT / "tests_data" / "expected_tiny.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def results(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("data")
    shutil.copytree(ROOT / "data" / "config", data_dir / "config")
    bank_exports = data_dir / "bank_exports"
    bank_exports.mkdir()
    shutil.copy(TINY_EXPORTS / "mono_tiny.csv", bank_exports / "monobank_tiny.csv")
    shutil.copy(TINY_EXPORTS / "privat_tiny.csv", bank_exports / "privatbank_tiny.csv")

    config = Config(str(data_dir))
    raw = load_data(config)
    clean_data, rejected = clean(raw)
    categorized = categorize(clean_data, config)

    expenses = categorized[categorized["amount_uah"] < 0]
    income = categorized[categorized["amount_uah"] > 0]

    expenses_by_category, expenses_by_month, _ = generate_analytics(expenses, None)
    income_by_category, _, _ = generate_analytics(income, None)

    return {
        "rows_read": len(raw),
        "valid_rows": len(raw) - len(rejected[rejected["rejection_reason"] == "Invalid value"]),
        "unique_transactions": len(categorized),
        "duplicates_removed": int((rejected["rejection_reason"] == "Duplicate entry").sum()),
        "invalid_rows": int((rejected["rejection_reason"] == "Invalid value").sum()),
        "expenses_by_category": {
            row["category"]: -row["total_expenses"] for _, row in expenses_by_category.iterrows()
        },
        "income_total": income_by_category["total_expenses"].sum(),
        "expenses_total": -expenses_by_month["total_expenses"].sum(),
    }


def test_row_counts(results):
    assert results["rows_read"] == EXPECTED["rows_read"]
    assert results["valid_rows"] == EXPECTED["valid_rows"]


def test_unique_duplicate_and_invalid_counts(results):
    assert results["unique_transactions"] == EXPECTED["unique_transactions"]
    assert results["duplicates_removed"] == EXPECTED["duplicates_removed"]
    assert results["invalid_rows"] == EXPECTED["invalid_rows"]


def test_expenses_by_category(results):
    assert results["expenses_by_category"] == pytest.approx(EXPECTED["expenses_by_category"])


def test_income_total(results):
    assert results["income_total"] == pytest.approx(EXPECTED["income_total"])


def test_expenses_total(results):
    assert results["expenses_total"] == pytest.approx(EXPECTED["expenses_total"])
