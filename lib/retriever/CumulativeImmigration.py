import pandas as pd

from lib.retriever.AbstractDataRetriever import AbstractDataRetriever
from lib.retriever.WorldBankDataRetriever import WorldBankDataRetriever


class CumulativeImmigration(AbstractDataRetriever):
    def __init__(self, min_year_range=None, max_year_range=None, ):
        super().__init__(
            keep_unit=True,
            data_name="Net Migration",
            round=0,
            source="https://data.worldbank.org/indicator/SM.POP.NETM",
            min_year_range=min_year_range or [1990, 1995],
            unit="%",
            max_year_range=max_year_range or [2023, 2023],
            show_final=True,
            description="Net migration is the net total of migrants during the period, that is, the number of immigrants minus the number of emigrants, including both citizens and noncitizens."
        )

    def retrieve(self, region):
        indicator = "SM.POP.NETM"
        retriever = WorldBankDataRetriever(indicator,
                                           min_year_range=self.min_year_range,
                                           max_year_range=self.max_year_range)
        data, data_column = retriever.retrieve(region)
        new_data = pd.DataFrame()
        year_from, year_to = retriever.good_years(data=data, data_column=data_column, region=region)
        for country in region.countries:
            country_data = data[
                (data["iso_a3"] == country.iso3) & (data["year"] >= year_from) & (data["year"] <= year_to)]
            if country_data[indicator].isna().any() or country.is_territory:
                continue
            new_data = pd.concat([new_data, pd.DataFrame({
                'iso_a3': [country.iso3],
                'year': [year_from],
                'data': [0.0]
            })])
            total_net_migration = sum(country_data[indicator])
            new_data = pd.concat([new_data, pd.DataFrame({
                'iso_a3': [country.iso3],
                'year': [year_to],
                'data': [total_net_migration]
            })])
        return new_data, "data"
