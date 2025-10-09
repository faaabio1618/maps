import numpy as np
import pandas as pd

from lib.AbstractDataRetriever import AbstractDataRetriever
from lib.Country import names_to_iso3, names_to_iso2


class DebtRetrieval(AbstractDataRetriever):

    def __init__(self, data_name, *,  is_rate=False, min_year_range=None, max_year_range=None):
        super().__init__(
            keep_unit=is_rate,
            min_year_range=min_year_range or [1995,1995],
            max_year_range=max_year_range or [2024,2024],
            unit = "%",
            data_name=data_name,
            round=0,
            show_final=True,
            description="Total stock of debt liabilities issued by the central government as a share of GDP.",
            source="https://www.imf.org/external/datamapper/CG_DEBT_GDP@GDD")
        self.min_year = 1995
        self.max_year = 2024

    def retrieve(self, region):
        csv_path = "data/debt.csv"
        data = pd.read_csv(csv_path)

        data = data.replace("no data", np.nan)

        data = data[data['country'].isin([country.name for country in region.countries])]

        data = data.melt(id_vars=['country'], var_name='year', value_name='debt')
        data['year'] = data['year'].astype(int)
        data['iso_a3'] = data['country'].map(names_to_iso3)
        data['iso_a2'] = data['country'].map(names_to_iso2)

        data = data[['country', 'year', 'debt', 'iso_a3']]
        # year_from = max(year_from, self.min_year)
        # year_to = min(year_to, self.max_year)
        year_from, year_to = self.min_year, self.max_year
        data = data[(data['year'] == year_from) | (data['year'] == year_to)]

        data['debt'] = pd.to_numeric(data['debt'].str.replace(',', '.', regex=False), errors='coerce')
        return data, 'debt'


# class AverageSalary(AbstractDataRetriever):
#
#     def __init__(self, data_name, is_rate=False, min_year_range=None, max_year_range=None):
#         super().__init__(data_name, is_rate, min_year_range or [1995], max_year_range or [2020])
#         self.min_year = 1995
#         self.max_year = 2020
#
#     def retrieve(self, countries):
#         data = pd.read_csv("data/salaries.csv")
#         data["iso_a3"] = data["REF_AREA"]
#         data = data[data['iso_a3'].isin([country.iso3 for country in countries])]
#
#         data["year"] = data["TIME_PERIOD"]
#         data["country"] = data["Reference area"]
#         data = data[['country', 'year', 'OBS_VALUE', 'iso_a3']]
#         data = data.sort_values(by=['country', 'year'])
#         year_from, year_to = self.min_year, self.max_year
#
#         data = data[(data['year'] == year_from) | (data['year'] == year_to)]
#
#         return self._format(data, "OBS_VALUE"), year_from, year_to
#
#     def customize_plot(self, bbox, ax, fig):
#         return ax, fig
#
#
# class LaborPerHour(AbstractDataRetriever):
#
#     def __init__(self, data_name, is_rate=False, min_year_range=None, max_year_range=None):
#         super().__init__(data_name, is_rate, min_year_range or [1993], max_year_range or [2019])
#         self.min_year = 1993
#         self.max_year = 2019
#
#     def retrieve(self, countries):
#         data = pd.read_csv("data/laborperhour.csv")
#         data["iso_a3"] = data["Code"]
#         data = data[data['iso_a3'].isin([country.iso3 for country in countries])]
#         year_from, year_to = self.min_year, self.max_year
#
#         data["year"] = data["Year"]
#         data["country"] = data["Entity"]
#         data = data[['country', 'year', 'productivity', 'iso_a3']]
#         data = data.sort_values(by=['country', 'year'])
#         data = data[(data['year'] == year_from) | (data['year'] == year_to)]
#
#         return self._format(data, "productivity"), year_from, year_to
#
#     def customize_plot(self, bbox, ax, fig):
#         return ax, fig
#
#
# class GiniCoefficientRetrieval(AbstractDataRetriever):
#
#     def __init__(self, data_name, is_rate=False, min_year_range=None, max_year_range=None):
#         super().__init__(data_name, is_rate, min_year_range or [1993], max_year_range or [2020])
#         self.min_year = 1993
#         self.max_year = 2020
#
#     def retrieve(self, countries):
#         data = pd.read_csv("data/economic-inequality-gini-index.csv")
#
#         data["country"] = data["Entity"]
#         data = data[data['country'].isin([country.name for country in countries])]
#
#         data["year"] = data["Year"]
#         data["iso_a2"] = data["country"].map(names_to_iso2)
#         data["gini"] = data["gini"] * 100
#
#         data['iso_a3'] = data['Code']
#         data = data[['country', 'year', 'gini', 'iso_a3']]
#         data['year'] = data['year'].astype(int)
#         data.columns = ['country', 'year', 'gini_coefficient', 'iso_a3']
#         data = data.sort_values(by=['country', 'year'])
#         year_from, year_to = self.min_year, self.max_year
#
#         for country in data['country'].unique():
#             values = data[data['country'] == country]['year'].values
#             if year_from not in values:
#                 for year in range(year_from - 3, year_from + 3):
#                     if year in values:
#                         data.loc[(data['country'] == country) & (data['year'] == year), 'year'] = year_from
#                         used_other_data = True
#                         break
#             if year_to not in values:
#                 for year in range(year_to - 3, year_to + 3):
#                     if year in values:
#                         data.loc[(data['country'] == country) & (data['year'] == year), 'year'] = year_to
#                         used_other_data = True
#                         break
#
#         data = data[(data['year'] == year_from) | (data['year'] == year_to)]
#
#         return self._format(data, "gini_coefficient"), year_from, year_to
#
#     def customize_plot(self, bbox, ax, fig):
#         ax.annotate(
#             "* Some countries do not have data for the selected years, so we used data from the closest available year.",
#             xy=(0.5, 0.05), xycoords='figure fraction',
#             ha="center", fontsize=10, color="black", alpha=0.8,
#             bbox=bbox
#         )
#         return ax, fig
