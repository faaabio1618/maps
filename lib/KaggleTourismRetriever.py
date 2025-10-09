from typing import Tuple

import pandas as pd

from lib.KaggleRetriever import KaggleRetriever


class KaggleTourismRetriever(KaggleRetriever):

    def __init__(self):
        super().__init__(
            keep_unit=False,
            data_name="Tourists Arrivals",
            source="https://www.kaggle.com/datasets/bushraqurban/tourism-and-economic-impact",
            min_year_range=[1999, 2000],
            max_year_range=[2018, 2019],
            unit="Arrivals",
            show_final=True,
            kaggle_handle="bushraqurban/tourism-and-economic-impact",
            file_names=["world_tourism_economy_data.csv"],
            round=0,
            description="The total number of international tourists who arrive in a country, measured in count."
        )

    def retrieve(self, region) -> Tuple[pd.DataFrame, str]:
        # https://www.kaggle.com/datasets/justin2028/arms-imports-per-country
        data = self._retrieve_kaggle(region)["world_tourism_economy_data.csv"]
        data["iso_a3"] = data["country_code"]
        return data, "tourism_arrivals"
