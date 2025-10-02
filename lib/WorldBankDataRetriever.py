import json
import os
import textwrap
from functools import wraps

import pandas as pd
from pandas_datareader import wb

from lib.AbstractDataRetriever import AbstractDataRetriever
from lib.Country import names_to_iso3

with open('data/indicators.json', encoding="utf-8") as f:
    indicators = json.load(f)[1]

dict_indicators = {ind["id"]: ind for ind in indicators}


class WorldBankDataRetriever(AbstractDataRetriever):

    def __init__(self, indicator, is_rate=False, min_year_range=None, max_year_range=None, round=0):
        indicator_ = dict_indicators[indicator]
        name_ = indicator_["name"]
        self.source_note = indicator_.get("sourceNote", "")
        if not is_rate:
            name_ = name_.split(' (')[0]
        super().__init__(
            data_name=name_,
            source  =  f"https://data.worldbank.org/indicator/{name_}",
            is_rate=is_rate,
            min_year_range=min_year_range or [1990, 1995],
            max_year_range=max_year_range or [2019, 2024],
            round=round)
        self.indicator = indicator

    def retrieve(self, countries):
        return self._retrieve_wb(countries)

    def _retrieve_wb(self, countries):
        if os.path.exists(f"./data/cache/wb_{self.indicator}.csv"):
            wb_data = pd.read_csv(f"./data/cache/wb_{self.indicator}.csv")
        else:
            wb_data = wb.download(indicator=self.indicator, country=[country.iso2 for country in countries],
                                  start=self.min_year_range[0], end=self.max_year_range[-1])
            os.makedirs("./data/cache", exist_ok=True)
            wb_data.to_csv(f"./data/cache/wb_{self.indicator}.csv")
        data = wb_data.reset_index()
        data = data[['country', 'year', self.indicator]]
        data['iso_a3'] = data['country'].map(names_to_iso3)
        data['year'] = data['year'].astype(int)
        data.columns = ['country', 'year', self.indicator, 'iso_a3']
        year_from, year_to = self.good_years(data, self.indicator)
        data = data[(data['year'] == year_from) | (data['year'] == year_to)]
        return self._format(data, self.indicator), year_from, year_to

    def customize_plot(self, bbox, ax, fig):
        note = textwrap.fill(self.source_note, width=40,max_lines=9 )
        if self.source_note:
            ax.annotate(
                f"{note}",
                xy=(0.700, 0.95), xycoords='figure fraction',
                va="top",
                ha="left", fontsize=10, color="black", alpha=0.8,
                bbox={**bbox, "facecolor": "lightgrey", "edgecolor": "grey", }
            )
        return ax, fig
