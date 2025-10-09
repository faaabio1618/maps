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

    def __init__(self, indicator, *, keep_unit=False, min_year_range=None, max_year_range=None, round=0,
                 show_final=True,
                 unit=None,
                 alternative_name=None):
        indicator_ = dict_indicators[indicator]
        name_ = alternative_name or indicator_["name"]
        split = name_.split(' (')
        try:
            unit_ = split[1].split(")")[0]
        except:
            unit_ = None
        unit = unit or unit_
        if not keep_unit:
            name_ = split[0]

        super().__init__(
            data_name=name_,
            source=f"https://data.worldbank.org/indicator/{indicator}",
            keep_unit=keep_unit,
            min_year_range=min_year_range or [1990, 1995],
            max_year_range=max_year_range or [2019, 2024],
            show_final=show_final,
            unit=unit,
            description=indicator_.get("sourceNote", ""),
            round=round)
        self.indicator = indicator

    def retrieve(self, region):
        return self._retrieve_wb(region)

    def _retrieve_wb(self, region):
        cachefile = f"./data/cache/{region.name}/wb_{self.indicator}.csv"
        if os.path.exists(cachefile):
            wb_data = pd.read_csv(cachefile)
        else:
            wb_data = wb.download(indicator=self.indicator, country=[iso2 for iso2 in region.iso2_list],
                                  # we download for all countries
                                  start=self.min_year_range[0], end=self.max_year_range[-1])
            os.makedirs(os.path.dirname(cachefile), exist_ok=True)
            wb_data.to_csv(cachefile)
        data = wb_data.reset_index()
        data = data[['country', 'year', self.indicator]]
        data['iso_a3'] = data['country'].map(names_to_iso3)
        data['year'] = data['year'].astype(int)
        data.columns = ['country', 'year', self.indicator, 'iso_a3']
        return data, self.indicator
