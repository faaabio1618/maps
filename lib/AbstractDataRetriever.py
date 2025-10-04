import abc
import os
from typing import Tuple

import cmocean
import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm

NA_LABEL = "//"


class AbstractDataRetriever(abc.ABC):
    """Abstract base class for data retrieval classes."""

    def __init__(self, *, data_name, source, is_rate=False, min_year_range=None, max_year_range=None, round=2,
                 ):
        self.data_name = data_name
        self.is_rate = is_rate
        self.min_year_range = min_year_range or [1990, 1996]
        self.max_year_range = max_year_range or [2019, 2024]
        self.round = round
        self.source = source

    @abc.abstractmethod
    def retrieve(self, region) -> Tuple[pd.DataFrame, int, int]:
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
    def customize_plot(self, *, region, bbox, ax, fig):
        pass

    def good_years(self, *, data, data_column, region) -> Tuple[int, int]:
        res = []
        # keep only countries in the region
        data = data[data['iso_a3'].isin([country.iso3 for country in region.countries])]
        # remove nan
        data = data[data[data_column].notna()]
        counts = {}
        for min_year in range(self.min_year_range[0], self.min_year_range[1] + 1):
            for max_year in range(self.max_year_range[0], self.max_year_range[1] + 1):
                data_filtered = data[(data['year'] == min_year) | (data['year'] == max_year)]
                data_filtered = data_filtered.groupby('iso_a3').filter(lambda x: len(x) == 2)
                counts[(min_year, max_year)] = len(data_filtered['iso_a3'].unique())

        max_count = max(counts.values())
        good_ranges = [k for k, v in counts.items() if v == max_count]
        # choose the widest range
        return max(good_ranges, key=lambda x: x[1] - x[0])

    def _file_name(self, *, year_from, year_to, region):
        return f"outputs/{region.name}/{year_from}/{year_to}/{self.data_name}.png"

    def plot(self, region, force=False):

        data, year_from, year_to = self.retrieve(region)
        # check if file exists
        filename = self._file_name(year_from=year_from, year_to=year_to, region=region)
        if not force:
            if os.path.exists(filename):
                print(f"{filename} already exists, skipping...")
                return
        file = "maps/ne_110m_admin_0_countries.zip"
        region_map = gpd.read_file(file)
        region_map = region_map.to_crs(region.crs)
        data_label = 'data'
        data = data[['iso_a3', data_label]]
        for iso3 in data['iso_a3'].unique():
            # we don't like naciscdn borders
            geometry = AbstractDataRetriever.__get_maps(iso3)
            geometry = geometry.to_crs(region_map.crs)
            region_map.loc[region_map['ADM0_A3'] == iso3, 'geometry'] = geometry["geometry"][0]

        disputed_territories = gpd.read_file("maps/ne_10m_admin_0_disputed_areas.zip")
        disputed_territories = disputed_territories.to_crs(region.crs)
        # filter by SOV_A3
        disputed_territories = disputed_territories[disputed_territories['ADM0_A3_FR'].isin(region.iso3_list)]

        data = region_map.merge(data, left_on='ADM0_A3', right_on='iso_a3', how='right')

        gdf = gpd.GeoDataFrame(data, geometry='geometry')

        minx = region.map_limits["minx"]
        maxx = region.map_limits["maxx"]
        miny = region.map_limits["miny"]
        maxy = region.map_limits["maxy"]

        gdf = gdf.cx[minx:maxx, miny:maxy]

        data_aspect = (maxy - miny) / (maxx - minx)
        dpi = 300
        fig_w = 12
        fig_h = fig_w * data_aspect
        fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h))
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.margins(1)

        # roi = roi = gpd.GeoDataFrame(geometry=[box(66, 22, 100, 39)], crs=region.cr
        disputed_territories.plot(ax=ax, facecolor="darkgray", edgecolor="white", hatch="///", linewidth=0)
        vals = gdf[data_label].to_numpy(dtype=float)  # we center at 0
        min_value = np.nanmin(vals)
        max_value = np.nanmax(vals)
        maxabs = np.nanpercentile(np.abs(vals), 92)
        minabs = np.nanpercentile(np.abs(vals), 8)
        vmin = -1 * maxabs
        vcenter = 0
        if vmin == 0:
            vcenter = 0.1
        norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=maxabs)
        schema = cmocean.cm.curl_r
        gdf.plot(column=data_label, ax=ax, legend=False, cmap=schema, norm=norm,
                 linewidth=0.5, edgecolor="0.7", antialiased=True,
                 missing_kwds={"color": "#e0e0e0", "edgecolor": "0.4", "label": NA_LABEL})

        for country_obj in region.countries:
            country = country_obj.iso3
            x, y = country_obj.label_coords(region)
            row = data.loc[data["iso_a3"] == country].iloc[0]
            if not x or not y:
                x, y = row.geometry.centroid.x, row.geometry.centroid.y
            label = row[data_label]
            value = np.nan if label == "nan" or np.isnan(label) else float(label)
            # print(f"{country}: {value} {x} {y}")

            if self.round == 0 and not np.isnan(label):
                label = str(int(value))
            custom_x, custom_y = country_obj.label_coords(region)
            if custom_x and custom_y:
                x, y = custom_x, custom_y

            label = str(label)
            if np.isnan(value):
                label = NA_LABEL
            else:
                if float(label) > 0:
                    label = "+" + label
                elif float(label) < 0:
                    # use true minus sign
                    label = "−" + label[1:]
                if not self.is_rate:
                    label = f"{label}%"

            #  label = country_obj.iso3
            # print(f'{country} {x} {y}')
            number_of_digits = len(str(value))
            font_size = country_obj.label_size - number_of_digits + self.round
            # if color is very dark, use white font
            bbox = {'facecolor': 'black', 'edgecolor': 'none', 'boxstyle': 'round,pad=0.2', 'alpha': 0.8}
            font_color = "white"
            if value == min_value or value == max_value:
                # make a bigger border
                bbox['edgecolor'] = "green"
                bbox["alpha"] = 1
                bbox['linewidth'] = 2

            ax.text(x, y, label, fontsize=font_size, ha='center', va='center',
                    color=font_color, alpha=1,
                    bbox=None if label == NA_LABEL else bbox)

        ax.set_title(f"{self.data_name}{' (change in %)' if not self.is_rate else ''}:  {year_from}→{year_to}",
                     fontsize=18)
        fig.tight_layout()
        xy, ha, va = region.source_position
        ax.annotate(
            f"Source: {self.source}",
            va=va,
            xy=xy, xycoords='figure fraction',
            ha=ha, fontsize=9, color="black", alpha=0.8,
            bbox={'facecolor': 'yellow', 'edgecolor': 'orange', 'boxstyle': 'round,pad=0.3', 'alpha': 0.9}
        )

        xy, ha, va = region.attribution_position
        ax.annotate(
            f"Graphics by u/fabio1618",
            xy=xy, xycoords='figure fraction',
            ha=ha, fontsize=8, color="black", alpha=0.8,
            va=va,
            bbox={'facecolor': "white", 'edgecolor': 'orange', 'boxstyle': 'round,pad=0.3', 'alpha': 0.9}
        )

        ax, fig = self.customize_plot(bbox={'facecolor': 'white', 'edgecolor': 'none', 'boxstyle': 'round,pad=0.2',
                                            'alpha': 0.5}, ax=ax, fig=fig, region=region)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        fig.savefig(filename, dpi=dpi)

    def _format(self, *, data, data_column, region):
        # add missing countries
        countries = region.countries
        year_from = min(data['year'].values)
        year_to = max(data['year'].values)
        missing_countries = [country for country in countries if country.iso3 not in data['iso_a3'].values]
        for country in missing_countries:
            if country:
                data = pd.concat([data, pd.DataFrame({
                    'iso_a3': [country.iso3],
                    'year': [year_from],
                    data_column: [np.nan]
                })], ignore_index=True)

        # remove countries not in the region
        data = data[data['iso_a3'].isin([country.iso3 for country in countries])]

        data = data.pivot(index='iso_a3', columns='year', values=data_column)
        data.columns = [f"{year}_{data_column}" for year in data.columns]
        data.reset_index(inplace=True)
        data['year_from'] = year_from
        data['year_to'] = year_to
        data['diff'] = data[f"{year_to}_{data_column}"] - data[f"{year_from}_{data_column}"]
        data_label = 'data'
        if self.is_rate:
            data[data_label] = data['diff']
        else:
            data[data_label] = (data[f"{year_to}_{data_column}"] / data[f"{year_from}_{data_column}"] - 1) * 100
            data[data_label] = data[data_label].replace(np.inf, np.nan)
            data[data_label] = data[data_label].replace(-np.inf, np.nan)
        data = data.round(self.round)
        return data
