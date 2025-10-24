import json
import os
from typing import Tuple

import pandas as pd
import requests

from lib import Country
from lib.retriever.AbstractDataRetriever import AbstractDataRetriever


class UnStatRetriever(AbstractDataRetriever):

    def __init__(self, *, source, unit, keep_unit, data_name, description, min_year_range, max_year_range, show_final,
                 series_description,
                 round,
                 category,
                 indicator: str):
        self.indicator = indicator
        self.series_description = series_description
        self.category = category
        super().__init__(
            max_year_range=min_year_range or [2019, 2024],
            min_year_range=max_year_range or [2000, 2001],
            show_final=show_final,
            data_name=data_name,
            description=description,
            source=source,
            unit=unit,
            round=round,
            keep_unit=keep_unit
        )

    def retrieve(self, region) -> Tuple[pd.DataFrame, str]:
        # check cache
        if os.path.exists(f"data/cache/un/{self.data_name}.json"):
            with open(f"data/cache/un/{self.data_name}.json", "r") as f:
                data = json.load(f)
                df = pd.DataFrame(data["data"])
        else:
            url = f"https://unstats.un.org/sdgapi/v1/sdg/Indicator/Data?indicator={self.indicator}"
            # retrive first page to calculate size
            r = requests.get(url)
            data = r.json()
            if data['data'] is None:
                raise Exception(f"No data found for indicator {self.indicator}")
            size = data['totalElements']
            whole_data_url = f"{url}&page=1&pageSize={size}"
            r = requests.get(whole_data_url, timeout=10000)
            os.makedirs(f"data/cache/un/", exist_ok=True)
            with open(f"data/cache/un/{self.data_name}.json", "w") as f:
                f.write(r.text)
            data = r.json()
            if data['data'] is None:
                raise Exception(f"No data found for indicator {self.indicator}")
            data = data["data"]
            df = pd.DataFrame(data)
        df["iso_a3"] = df["geoAreaName"].map(Country.names_to_iso3)
        df = df[
            df["seriesDescription"].fillna("").astype(str).str.strip().str.contains(self.series_description, case=False,
                                                                                    regex=False)]
        df = df[df["dimensions"].fillna("").astype(str).str.strip().str.contains(self.category, case=False, regex=False)]
        df["year"] = df["timePeriodStart"].astype(int)
        df["value"] = df["value"].astype(float)
        df = df[["iso_a3", "year", "value"]]
        df = df[df["iso_a3"].notna()]
        df = df[df["iso_a3"].isin(region.iso3_list)]
        return df, "value"
