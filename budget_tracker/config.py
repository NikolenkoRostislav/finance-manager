import json
from pathlib import Path


class UsdToUahExchange:
    def __init__(self, uah: float, usd: float):
        if uah is None or usd is None or uah <= 0 or usd <= 0:
            raise ValueError("Invalid exchange rates.")
        self.rate = usd / uah

    def usd_to_uah(self, amount: float) -> float:
        return amount * self.rate


class Config:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        exchange_rates_path = self.data_path / "config" / "exchange_rates.json"
        categories_rules_path = self.data_path / "config"/ "categories_rules.json"

        with open(exchange_rates_path, "r", encoding='utf-8') as f:
            self.exchange = json.load(f)
            self.exchange = UsdToUahExchange(uah=self.exchange.get("UAH"), usd=self.exchange.get("USD"))

        with open(categories_rules_path, "r", encoding='utf-8') as f:
            self.categories_rules = json.load(f)
            self.categories_rules = self.categories_rules.get("rules", [])

__all__ = ["Config"]
