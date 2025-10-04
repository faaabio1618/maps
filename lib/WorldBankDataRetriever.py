import json
import os
import textwrap

import pandas as pd
from pandas_datareader import wb

from lib.AbstractDataRetriever import AbstractDataRetriever
from lib.Country import names_to_iso3, Country

with open('data/indicators.json', encoding="utf-8") as f:
    indicators = json.load(f)[1]

dict_indicators = {ind["id"]: ind for ind in indicators}


class WorldBankDataRetriever(AbstractDataRetriever):

    def __init__(self, indicator, *, is_rate=False, min_year_range=None, max_year_range=None, round=0):
        indicator_ = dict_indicators[indicator]
        name_ = indicator_["name"]
        self.source_note = indicator_.get("sourceNote", "")
        if not is_rate:
            name_ = name_.split(' (')[0]
        super().__init__(
            data_name=name_,
            source=f"https://data.worldbank.org/indicator/{indicator}",
            is_rate=is_rate,
            min_year_range=min_year_range or [1990, 1995],
            max_year_range=max_year_range or [2019, 2024],
            round=round)
        self.indicator = indicator

    def retrieve(self, region):
        return self._retrieve_wb(region)

    def _retrieve_wb(self, region):
        if os.path.exists(f"./data/cache/wb_{self.indicator}.csv"):
            wb_data = pd.read_csv(f"./data/cache/wb_{self.indicator}.csv")
        else:
            wb_data = wb.download(indicator=self.indicator, country=[country.iso2 for country in Country.all()],
                                  # we download for all countries
                                  start=self.min_year_range[0], end=self.max_year_range[-1])
            os.makedirs("./data/cache", exist_ok=True)
            wb_data.to_csv(f"./data/cache/wb_{self.indicator}.csv")
        data = wb_data.reset_index()
        data = data[['country', 'year', self.indicator]]
        data['iso_a3'] = data['country'].map(names_to_iso3)
        data['year'] = data['year'].astype(int)
        data.columns = ['country', 'year', self.indicator, 'iso_a3']
        year_from, year_to = self.good_years(data=data, data_column=self.indicator, region=region)
        mask_from = data['year'].between(max(year_from - 1, self.min_year_range[0]),
                                         min(self.min_year_range[1], year_from + 1))
        mask_to = data['year'].between(max(year_to - 1, self.max_year_range[0]),
                                       min(self.max_year_range[1], year_to + 1))
        data = data[mask_from | mask_to]
        for country in region.iso3_list:
            values = data.loc[(data['iso_a3'] == country) & (data[self.indicator].notna()), 'year'].values
            has_year_from = any(year_from - 1 <= year <= year_from + 1 for year in values)
            har_year_to = any(year_to - 1 <= year <= year_to + 1 for year in values)
            if (year_from not in values or year_to not in values) and (has_year_from and har_year_to):
                self.partial_countries.append(Country.get_by_iso3(country))

        return self._format(data=data, data_column=self.indicator, region=region), year_from, year_to

    def customize_plot(self, *, region, bbox, ax, fig):
        if len(self.partial_countries) > 0:
            note = "**Countries with values in parentheses use data from adjacent years.**    \n" + self.source_note
        else:
            note = self.source_note
        note = textwrap.fill(note, width=40, max_lines=9, placeholder="... [See more at source]", replace_whitespace=False,)
        xy, ha, va = region.description_position
        if self.source_note:
            ax.annotate(
                f"{note}",
                xy=xy, xycoords='figure fraction',
                va=va,
                ha=ha, fontsize=10, color="black", alpha=0.8,
                bbox={**bbox, "facecolor": "lightgrey", "edgecolor": "grey", }
            )
        return ax, fig
