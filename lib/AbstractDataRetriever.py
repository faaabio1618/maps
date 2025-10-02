import abc
import os
from typing import List, Tuple

import cmocean
import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm

from lib.Country import Country


class AbstractDataRetriever(abc.ABC):
    """Abstract base class for data retrieval classes."""

    def __init__(self, *, data_name, source, is_rate=False, min_year_range=None, max_year_range=None, round=2):
        if max_year_range is None:
            max_year_range = [2019, 2024]
        if min_year_range is None:
            min_year_range = [1990, 1996]
        self.data_name = data_name
        self.is_rate = is_rate
        self.min_year_range = min_year_range
        self.max_year_range = max_year_range
        self.round = round
        self.source = source

    @abc.abstractmethod
    def retrieve(self, countries: List[Country]) -> Tuple[pd.DataFrame, int, int]:
        pass

    @staticmethod
    def __get_maps(iso3):
        if os.path.exists(f"maps/gadm41_{iso3}_0.json"):
            return gpd.read_file(f"maps/gadm41_{iso3}_0.json")
        else:
            print(f"Could not find map of {iso3}")
            url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{iso3}_0.json"
            # save json to maps folder
            os.makedirs("maps", exist_ok=True)
            r = requests.get(url)
            with open(f"maps/gadm41_{iso3}_0.json", "wb") as f:
                f.write(r.content)
            return AbstractDataRetriever.__get_maps(iso3)

    @abc.abstractmethod
    def customize_plot(self, bbox, ax, fig):
        pass

    def good_years(self, data, data_column) -> Tuple[int, int]:
        res = []
        for r, fun in [(self.min_year_range, min), (self.max_year_range, max)]:
            counts = {}
            for year in range(r[0], r[1] + 1):
                if year in data['year'].values:
                    counts[year] = data[data['year'] == year][data_column].count()
            if len(counts) == 0:
                raise ValueError(f"No data found for any year in range {r}")

            max_value = max(counts.values())
            good_years = [year for year, count in counts.items() if count == max_value]
            res.append(fun(good_years))
        return res[0], res[1]

    def plot(self, force=False):

        countries = Country.all()
        data, year_from, year_to = self.retrieve(countries)
        # check if file exists
        if not force:
            if os.path.exists(f"outputs/{year_from}/{year_to}/{self.data_name}.png"):
                print(f"File outputs/{year_from}/{year_to}/{self.data_name}.png already exists, skipping...")
                return
        file = "maps/ne_110m_admin_0_countries.zip"
        europe = gpd.read_file(file)
        europe = europe.to_crs(3035)
        data = data[['iso_a3', '%_change']]
        for iso3 in data['iso_a3'].unique():
            # we don't like naciscdn borders
            geometry = AbstractDataRetriever.__get_maps(iso3)
            geometry = geometry.to_crs(3035)
            europe.loc[europe['ADM0_A3'] == iso3, 'geometry'] = geometry["geometry"][0]

        data = europe.merge(data, left_on='ADM0_A3', right_on='iso_a3', how='right')
        gdf = gpd.GeoDataFrame(data, geometry='geometry')

        minx = 2600000
        maxx = 7700000
        miny = 1440000
        maxy = 5500000

        gdf = gdf.cx[minx:maxx, miny:maxy]

        data_aspect = (maxy - miny) / (maxx - minx)
        fig_w = 12
        fig_h = fig_w * data_aspect
        fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h))
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.margins(1)

        vals = gdf['%_change'].to_numpy(dtype=float)  # we center at 0
        min_value = np.nanmin(vals)
        max_value = np.nanmax(vals)
        maxabs = np.nanpercentile(np.abs(vals), 92)
        minabs = np.nanpercentile(np.abs(vals), 8)
        vmin = -1 * maxabs
        vcenter = 0
        if vmin == 0:
            vcenter = 0.1
        norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=maxabs)
        gdf.plot(column='%_change', ax=ax, legend=False, cmap=cmocean.cm.delta, norm=norm,
                 linewidth=0.5, edgecolor="0.7", antialiased=True,
                 missing_kwds={"color": "#e0e0e0", "edgecolor": "0.4", "label": "///"})

        for x, y, label, country in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y,
                                        gdf['%_change'].astype(str), gdf["iso_a3"]):

            value = np.nan if label == "nan" else float(label)
            # print(f"{country}: {value} {x} {y}")

            if self.round == 0 and label != "nan":
                label = str(int(value))
            country_obj = Country.get_by_iso3(country)
            custom_x, custom_y = country_obj.label_coords
            if custom_x and custom_y:
                x, y = custom_x, custom_y

            if label == "nan":
                label = "///"
            else:
                if float(label) > 0:
                    label = "+" + label
                if not self.is_rate:
                    label = f"{label}%"

            number_of_digits = len(str(value))
            font_size = country_obj.label_size - number_of_digits + self.round
            # if color is very dark, use white font
            bbox = {'facecolor': 'black', 'edgecolor': 'none', 'boxstyle': 'round,pad=0.2', 'alpha': 0.7}
            font_color = "white"
            if value == min_value or value == max_value:
                # make a bigger border
                bbox['edgecolor'] = "green"
                bbox["alpha"] = 1
                bbox['linewidth'] = 2

            ax.text(x, y, label, fontsize=font_size, ha='center', va='center',
                    color=font_color, alpha=1,
                    bbox=None if label == "///" else bbox)

        ax.set_title(f"{self.data_name}{' (change in %)' if not self.is_rate else ''}:  {year_from}→{year_to}", fontsize=16,)
        fig.tight_layout()
        ax.annotate(
            f"Source: {self.source}",
            va="top",
            xy=(0.035, 0.95), xycoords='figure fraction',
            ha="left", fontsize=10, color="black", alpha=0.8,
        bbox = {'facecolor': 'yellow', 'edgecolor': 'orange', 'boxstyle': 'round,pad=0.3', 'alpha': 0.9}
        )

        ax.annotate(
            f"Graphics by u/fabio1618",
            xy=(0.965, 0.03), xycoords='figure fraction',
            ha="right", fontsize=8, color="black", alpha=0.8,
            bbox = {'facecolor': "white", 'edgecolor': 'orange', 'boxstyle': 'round,pad=0.3', 'alpha': 0.9}
        )

        ax, fig = self.customize_plot(bbox={'facecolor': 'white', 'edgecolor': 'none', 'boxstyle': 'round,pad=0.2',
                                            'alpha': 0.5}, ax=ax, fig=fig)
        # mkdir outputs/yearfrom/yearto
        os.makedirs(f"outputs/{year_from}/{year_to}", exist_ok=True)
        fig.savefig(f"outputs/{year_from}/{year_to}/{self.data_name}.png", dpi=300)

    def _format(self, data, data_column):
        # add missing countries
        missing_countries = [country for country in Country.all() if country.iso3 not in data['iso_a3'].values]
        for country in missing_countries:
            if country:
                data = pd.concat([data, pd.DataFrame({
                    'iso_a3': [country.iso3],
                    'year': [self.min_year_range[0]],
                    data_column: [np.nan]
                })], ignore_index=True)
        data = data.pivot(index='iso_a3', columns='year', values=data_column)
        year_from = min(data.columns)
        year_to = max(data.columns)
        data.columns = [f"{year}_{data_column}" for year in data.columns]
        data.reset_index(inplace=True)
        data['year_from'] = year_from
        data['year_to'] = year_to
        data['diff'] = data[f"{year_to}_{data_column}"] - data[f"{year_from}_{data_column}"]
        if self.is_rate:
            data['%_change'] = data['diff']
        else:
            data['%_change'] = (data[f"{year_to}_{data_column}"] / data[f"{year_from}_{data_column}"] - 1) * 100
            data['%_change'] = data['%_change'].replace(np.inf, np.nan)
            data['%_change'] = data['%_change'].replace(-np.inf, np.nan)
        data = data.round(self.round)
        return data
