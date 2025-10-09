from typing import Tuple
import pandas

import pandas as pd

from lib.AbstractDataRetriever import AbstractDataRetriever


class EconomicFreedomRetriever(AbstractDataRetriever):

    def __init__(self, from_year=1995, to_year=2023):
        self.from_year = from_year
        self.to_year = to_year
        super().__init__(
            min_year_range=[from_year, from_year],
            keep_unit=True,
            unit = None,
            max_year_range=[to_year, to_year],
            show_final=True,
            description="Economic freedoms are a subset of human freedoms and concern economic activities such as working, transacting, contracting with others, and owning and using productive property. Individuals are more economically free when they are allowed to make more of their own economic choices. Their choices, however, must respect the rights of others.",
            data_name="Economic Freedom Summary Index",
            source="https://efotw.org/?geozone=world&page=map&year=2023"
        )

    def retrieve(self, region) -> Tuple[pd.DataFrame, str]:
        data_from = pandas.read_csv(f"data/economicdata{self.from_year}-{self.from_year}.csv")
        data_to = pandas.read_csv(f"data/economicdata{self.to_year}-{self.to_year}.csv")
        data = pd.concat([data_from, data_to])
        data["year"] = data["Year"]
        data["iso_a3"] = data["ISO_Code"]
        return data, "Economic Freedom Summary Index"
