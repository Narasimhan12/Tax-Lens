from __future__ import annotations

import pandas as pd

from app.config import settings
from app.models.schemas import CompanyTaxInput


class CompanyRepository:
    def __init__(self) -> None:
        self.df = pd.read_csv(settings.dataset_path)
        self.df["CompanyNameNormalized"] = self.df["CompanyName"].str.lower().str.strip()

    def list_company_names(self) -> list[str]:
        return sorted(self.df["CompanyName"].tolist())

    def get_company(self, company_name: str) -> CompanyTaxInput:
        normalized = company_name.lower().strip()
        row = self.df[self.df["CompanyNameNormalized"] == normalized]
        if row.empty:
            raise ValueError(f"Company not found: {company_name}")
        record = row.iloc[0].drop(labels=["CompanyNameNormalized"]).to_dict()
        return CompanyTaxInput(**record)
