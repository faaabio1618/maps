import pandas as pd

from lib.AbstractDataRetriever import AbstractDataRetriever
from lib.WorldBankDataRetriever import WorldBankDataRetriever


class CumulativeInflation(AbstractDataRetriever):

    def __init__(self):
        super().__init__(
            keep_unit=True,
            data_name="Cumulative inflation",
            source="https://www.worldbank.org/data/indicator/SI.XPD.CHEX.GD.ZS",
            min_year_range=[1990, 1995],
            unit=None,
            max_year_range=[2023, 2023],
            show_final=True,
            description="Inflation as measured by the consumer price index reflects the annual percentage change in the cost to the average consumer of acquiring a basket of goods and services that may be fixed or changed at specified intervals, such as yearly. This indicator denotes the percentage change over each previous year of the constant price (base year 2015) series in United States dollars."
        )

    def retrieve(self, region):
        indicator = "FP.CPI.TOTL.ZG"
        retriever = WorldBankDataRetriever(indicator,
                                           min_year_range=self.min_year_range,
                                           max_year_range=self.max_year_range)
        data, data_column = retriever.retrieve(region)
        year_from, year_to = retriever.good_years(data=data, data_column=data_column, region=region)
        # compound inflation from year_from to year_to, skip countries with missing data
        new_data = pd.DataFrame()
        for country in region.countries:
            country_data = data[
                (data["iso_a3"] == country.iso3) & (data["year"] >= year_from) & (data["year"] <= year_to)]
            if country_data[indicator].isna().any():
                continue
            new_data = pd.concat([new_data, pd.DataFrame({
                'iso_a3': [country.iso3],
                'year': [year_from],
                'data': [0.0]
            })])
            inflation_rate = 1.0
            for rate in country_data[indicator]:
                inflation_rate *= (1 + rate / 100)
            cumulative_inflation = (inflation_rate - 1) * 100
            new_data = pd.concat([new_data, pd.DataFrame({
                'iso_a3': [country.iso3],
                'year': [year_to],
                'data': [cumulative_inflation]
            })])
        return new_data, "data"
