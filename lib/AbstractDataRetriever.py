import abc
import os
import textwrap
from typing import Tuple

import cmocean
import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.offsetbox import TextArea, AnnotationBbox

from lib.Country import Country

NA_LABEL = None
DATA_LABEL = 'data'
FINAL_LABEL = 'final_value'
YELLOW = "#fceaa9"


def human_format(num: float):
    magnitude = 0
    rounding = 0 if 100 < num < 10 ** 9 else 1
    while abs(num) >= 1000 and magnitude < 4:
        magnitude += 1
        num /= 1000.0
    num = round(num, rounding)
    suffixes = ['', 'K', 'M', 'B', 'T']
    num_str = f"{num:.{rounding}f}".rstrip('0').rstrip('.')
    if num_str in ('-0', '-0.0', '0.0'):
        num_str = '0'
    return f"{num_str}{suffixes[magnitude]}"


class AbstractDataRetriever(abc.ABC):
    """Abstract base class for data retrieval classes."""

    def __init__(self, *, data_name, source, description, unit, keep_unit=False, min_year_range=None,
                 max_year_range=None,
                 round=2,
                 show_final=False):
        if not data_name:
            raise ValueError("data_name must be provided")
        if not source:
            raise ValueError("source must be provided")
        if min_year_range and (len(min_year_range) != 2 or min_year_range[0] > min_year_range[1]):
            raise ValueError("min_year_range must be a list of two years [min, max] with min < max")
        if max_year_range and (len(max_year_range) != 2 or max_year_range[0] > max_year_range[1]):
            raise ValueError("max_year_range must be a list of two years [min, max] with min < max")
        self.data_name = data_name
        self.keep_unit = keep_unit
        self.min_year_range = min_year_range or [1990, 1996]
        self.max_year_range = max_year_range or [2018, 2024]
        self.round = round
        self.source = source
        self.description = description
        self.unit = unit
        self.partial_countries = []
        self.show_final = show_final

    @abc.abstractmethod
    def retrieve(self, region) -> Tuple[pd.DataFrame, str]:
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

    def good_years(self, *, data, data_column, region) -> Tuple[int, int]:
        res = []
        # keep only countries in the region
        data = data[data['iso_a3'].isin([country.iso3 for country in region.countries])]
        # remove nan
        data = data[data[data_column].notna()]
        counts = {}
        min_years = range(self.min_year_range[0], self.min_year_range[1] + 1)
        max_years = range(self.max_year_range[0], self.max_year_range[1] + 1)
        for min_year in min_years:
            for max_year in max_years:
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

        data, data_column = self.retrieve(region)
        data, year_from, year_to = self.apply_diff(data=data, data_column=data_column, region=region)
        filename = self._file_name(year_from=year_from, year_to=year_to, region=region)
        if not force:
            if os.path.exists(filename):
                print(f"{filename} already exists, skipping...")
                return filename
            else:
                print(f"Creating {filename}...")
        file = "maps/ne_110m_admin_0_countries.zip"
        region_map = gpd.read_file(file)
        region_map = region_map.to_crs(region.crs)
        data = data[['iso_a3', DATA_LABEL, FINAL_LABEL]]
        for iso3 in region.iso3_list:
            # we don't like naciscdn borders
            geometry = AbstractDataRetriever.__get_maps(iso3)
            geometry = geometry.to_crs(region_map.crs)
            if (region_map['ADM0_A3'] == iso3).any():
                region_map.loc[region_map['ADM0_A3'] == iso3, 'geometry'] = geometry['geometry'].iloc[0]
            else:
                new_row = gpd.GeoDataFrame(
                    {'ADM0_A3': [iso3], 'geometry': [geometry['geometry'].iloc[0]]},
                    crs=region_map.crs
                )
                region_map = pd.concat([region_map, new_row], ignore_index=True)
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
        fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h), dpi=dpi)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.margins(1)

        disputed_territories.plot(ax=ax, facecolor="darkgray", edgecolor="white", hatch="///", linewidth=0)
        countries_to_show = [country.iso3 for country in region.countries if country.show_value]
        vals = gdf[gdf['ADM0_A3'].isin(countries_to_show)][DATA_LABEL].to_numpy(dtype=float)  # we center at 0
        min_value = np.nanmin(vals)
        max_value = np.nanmax(vals)
        maxabs = np.nanpercentile(np.abs(vals), 92)
        # minabs = np.nanpercentile(np.abs(vals), 8)
        vmin = -1 * maxabs
        vcenter = 0
        if vmin == 0:
            vcenter = 0.1
        norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=maxabs)
        schema = cmocean.cm.curl_r
        gdf.plot(column=DATA_LABEL, ax=ax, legend=False, cmap=schema, norm=norm,
                 linewidth=0.5, edgecolor="0.7", antialiased=True,
                 missing_kwds={"color": "#e0e0e0", "edgecolor": "0.7", "label": NA_LABEL})
        # exclude countries where show_value is False

        for country_obj in region.countries:
            if not country_obj.show_value:
                continue
            country = country_obj.iso3
            x, y = country_obj.label_coords(region)
            row = data.loc[data["iso_a3"] == country].iloc[0]
            if not x or not y:
                x, y = row.geometry.centroid.x, row.geometry.centroid.y
            label = row[DATA_LABEL]
            final_value = row[FINAL_LABEL]
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
                if not self.keep_unit:
                    label = f"{label}%"
                if country_obj in self.partial_countries:
                    label = f"({label})"

            # label = country_obj.iso3
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

        fig.suptitle(f"{self.data_name}{' (change in %)' if not self.keep_unit else ''}:  {year_from}→{year_to}",
                     fontsize=19,
                     bbox={'facecolor': 'white', 'edgecolor': 'none', 'boxstyle': 'round,pad=0.2', 'alpha': 0.8},
                     y=0.994)

        ax, fig, ranks = self.__add_ranks_and_description(data=data, year_to=year_to, region=region, ax=ax, fig=fig)
        ax, fig = self.__add_source(region=region, ax=ax, fig=fig)
        ax, fig = self.__add_attribution(region=region, ax=ax, fig=fig)
        fig.tight_layout()
        ax.margins(0)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.set_axis_off()
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        fig.savefig(filename, dpi=dpi, pad_inches=0.12, bbox_inches='tight',
                    bbox_extra_artists=[ranks] if self.show_final else None)
        plt.close(fig)
        return filename

    def __add_ranks_and_description(self, *, data, year_to, region, ax, fig):
        ranks = None
        new_margin = 1
        side = region.rank_position
        if self.show_final:
            final_values = []
            for country_obj in region.countries:
                if not country_obj.show_value:
                    continue
                country = country_obj.iso3
                row = data.loc[data["iso_a3"] == country].iloc[0]
                final_value = row[FINAL_LABEL]
                if np.isnan(final_value):
                    continue
                human_value = human_format(final_value)
                final_values.append((country, final_value, human_value))
            title = f"   {year_to}   "
            sorted_final_values = sorted(final_values, key=lambda x: float(x[1]))
            sorted_final_values = [f"{iso} ≈ {human}" for iso, value, human in sorted_final_values]
            max_length_value = max(len(title), max([len(str(final_value)) for final_value in sorted_final_values]))
            final_values = "\n".join(sorted_final_values)
            if side == "left":
                new_margin = max_length_value * -1 / 1000 * 7
            else:
                new_margin = 1.03 + (5 * max_length_value) / 1000

            year_to_s = str(year_to).center(max_length_value)
            text = f"{year_to_s}\n"
            if self.unit:
                unit = textwrap.fill(self.unit, width=max_length_value)
                unit = "\n".join(map(lambda l: l.center(max_length_value), unit.splitlines()))
                text = text + f"{unit}\n\n"
            else:
                text = text + "\n"
            text = text + f"{final_values}"
            text_area = TextArea(text,
                                 textprops={'color': 'black', "ha": "left", "fontfamily": "monospace", "fontsize": 9})
            annotation_box = AnnotationBbox(
                text_area, (new_margin, 0.995), xycoords=ax.transAxes,
                boxcoords=ax.transAxes,
                box_alignment=(0 if side == "left" else 1, 1),
                pad=0,
                bboxprops={'facecolor': YELLOW, 'edgecolor': (0, 0, 0, 1), "linewidth": 0, 'boxstyle': 'round,pad=0.4',
                           'alpha': 1},
            )
            ranks = ax.add_artist(annotation_box)

        # description
        if len(self.partial_countries) > 0:
            note = "**Countries with values in parentheses use data from adjacent years.**    \n" + self.description
        else:
            note = self.description
        note = textwrap.fill(note, width=40, max_lines=9, placeholder="... [See more at source]",
                             replace_whitespace=False, )
        xy, ha, va = region.description_position
        xy = (new_margin, xy[1])
        text_area = TextArea(note, textprops={'color': 'black', "ha": "left", "fontsize": 11})
        annotation_box = AnnotationBbox(
            text_area, xy, xycoords=ax.transAxes,
            boxcoords=ax.transAxes,
            box_alignment=(1 if side == "right" else 0, 0),
            bboxprops={'facecolor': YELLOW, 'edgecolor': 'none', 'boxstyle': 'round,pad=0.2', 'alpha': 1},
        )
        if self.description:
            ax.add_artist(annotation_box)
        return ax, fig, ranks

    def __add_source(self, *, region, ax, fig):
        xy, ha, va = region.source_position
        text = TextArea(f"Source: {self.source}", textprops={'color': 'black', "ha": "left", "fontsize": 9})
        annotation_box = AnnotationBbox(
            text, xy, xycoords=ax.transAxes,
            boxcoords=ax.transAxes,
            box_alignment=(0 if ha == "left" else 1, 0 if va == "bottom" else 0),
            bboxprops={'facecolor': YELLOW, 'edgecolor': 'orange', 'boxstyle': 'round,pad=0.3', 'alpha': 0.9}
        )
        ax.add_artist(annotation_box)
        return ax, fig

    def __add_attribution(self, *, region, ax, fig):
        xy, ha, va = region.attribution_position
        text = TextArea("by u/fabio1618", textprops={'color': 'black', "ha": "right", "fontsize": 8})
        annotation_box = AnnotationBbox(
            text, xy, xycoords=ax.transAxes,
            boxcoords=ax.transAxes,
            box_alignment=(0 if ha == "left" else 1, 1 if va == "top" else 0),
            bboxprops={'facecolor': "white", 'edgecolor': 'orange', 'boxstyle': 'round,pad=0.3', 'alpha': 0.9}
        )
        ax.add_artist(annotation_box)
        return ax, fig

    def _adjacent_years(self, *, data, region, data_column, year_from, year_to, ):
        mask_from = data['year'].between(max(year_from - 1, self.min_year_range[0]),
                                         min(self.min_year_range[1], year_from + 1))
        mask_to = data['year'].between(max(year_to - 1, self.max_year_range[0]),
                                       min(self.max_year_range[1], year_to + 1))
        data = data[mask_from | mask_to]
        for country in region.iso3_list:
            values = data.loc[(data['iso_a3'] == country) & (data[data_column].notna()), 'year'].values
            has_year_from = any(year_from - 1 <= year <= year_from + 1 for year in values)
            har_year_to = any(year_to - 1 <= year <= year_to + 1 for year in values)
            if (year_from not in values or year_to not in values) and (has_year_from and har_year_to):
                self.partial_countries.append(Country.get_by_iso3(country))
        return data

    def apply_diff(self, *, data, data_column, region) -> Tuple[pd.DataFrame, int, int]:
        year_from, year_to = self.good_years(data=data, data_column=data_column, region=region)
        data = self._adjacent_years(data=data, region=region, data_column=data_column, year_from=year_from,
                                    year_to=year_to)
        countries = region.countries
        data = data[data['iso_a3'].isin([country.iso3 for country in countries])]
        data = data[data[data_column].notna()]
        data["is_year_to"] = data["year"] == year_to
        data["is_year_from"] = data["year"] == year_from
        data["has_year_to"] = data.groupby("iso_a3")["is_year_to"].transform("max")
        data["has_year_from"] = data.groupby("iso_a3")["is_year_from"].transform("max")

        data["min_year"] = data.groupby("iso_a3")["year"].transform("min")
        data["max_year"] = data.groupby("iso_a3")["year"].transform("max")
        # if a country has year to replace min_year with year_to
        data.loc[(data["has_year_to"]), "min_year"] = year_from
        # if a country has year from replace max_year with year_from
        data.loc[(data["has_year_from"]), "max_year"] = year_to
        data = data[(data["min_year"] >= self.min_year_range[0]) & (data["min_year"] <= self.min_year_range[1])]
        data = data[(data["max_year"] >= self.max_year_range[0]) & (data["max_year"] <= self.max_year_range[1])]

        data = data[(data['year'] == data["min_year"]) | (data['year'] == data["max_year"])]
        data = data.drop(columns=["min_year", "max_year"])

        missing_countries = [country for country in countries if country.iso3 not in data['iso_a3'].values]
        for country in missing_countries:
            if country:
                data = pd.concat([data, pd.DataFrame({
                    'iso_a3': [country.iso3],
                    'year': [year_from],
                    data_column: [np.nan]
                })], ignore_index=True)

        data.loc[
            (data['year'] >= self.min_year_range[0]) & (data['year'] <= self.min_year_range[1]), 'year'] = year_from
        data.loc[(data['year'] >= self.max_year_range[0]) & (data['year'] <= self.max_year_range[1]), 'year'] = year_to

        data = data.pivot(index='iso_a3', columns='year', values=data_column)
        data.columns = [f"{year}_{data_column}" for year in data.columns]
        data.reset_index(inplace=True)
        data['year_from'] = year_from
        data['year_to'] = year_to
        data['diff'] = data[f"{year_to}_{data_column}"] - data[f"{year_from}_{data_column}"]
        data[FINAL_LABEL] = data[f"{year_to}_{data_column}"]
        data_label = 'data'
        if self.keep_unit:
            data[data_label] = data['diff']
        else:
            data[data_label] = (data[f"{year_to}_{data_column}"] / data[f"{year_from}_{data_column}"] - 1) * 100
            data[data_label] = data[data_label].replace(np.inf, np.nan)
            data[data_label] = data[data_label].replace(-np.inf, np.nan)
        data[data_label] = data[data_label].round(self.round)
        return data, year_from, year_to
