import os
from typing import Tuple

import kagglehub
import pandas as pd
from kagglehub import KaggleDatasetAdapter

from lib.Country import Country
from lib.KaggleRetriever import KaggleRetriever


class KaggleAverageTemperatureRetriever(KaggleRetriever):

    def __init__(self):
        super().__init__(
            keep_unit=True,
            data_name="Mean Annual Temperature (C°)",
            source="https://climateknowledgeportal.worldbank.org/index.php/explore \nThrough: https://www.kaggle.com/datasets/palinatx/mean-temperature-for-countries-by-year-2014-2022",
            min_year_range=[1990, 1995],
            unit = 'C°',
            description="Average Mean Surface Air Temperature",
            show_final=True,
            max_year_range=[2020, 2024],
            kaggle_handle="palinatx/mean-temperature-for-countries-by-year-2014-2022",
            file_names=["combined_temperature.csv"],
            round=1
        )

    def retrieve(self, region) -> Tuple[pd.DataFrame, str]:
        datas = self._retrieve_kaggle(region)
        data = datas["combined_temperature.csv"]
        data["iso_a3"] = data["Country"].map(lambda c:Country.get_by_name(c).iso3 if Country.get_by_name(c) else None)
        # for some reason KOR is repeated twice for each year, drop one
        data = data.drop_duplicates(subset=["iso_a3", "Year"], keep="first")

        data = data.rename(columns={"Year": "year"})
        return data, "Annual Mean"
