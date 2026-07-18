import os
import unittest
from types import SimpleNamespace

import pandas as pd

from lib.Country import Country
from lib.Map import Map
from lib.retriever.AbstractDataRetriever import (
    AdaptiveDivergingNorm,
    AbstractDataRetriever,
    CHANGE_SCALE_COLORS,
    MAP_STYLE_VERSION,
    format_map_value,
)


class DummyRetriever(AbstractDataRetriever):
    def __init__(self):
        super().__init__(
            data_name="Test data",
            source="test",
            description="",
            unit="units",
            keep_unit=True,
            min_year_range=[1990, 1991],
            max_year_range=[2019, 2020],
        )

    def retrieve(self, region):
        raise NotImplementedError


class P0RegressionTests(unittest.TestCase):
    def test_change_scale_uses_blue_neutral_and_gold_without_red_or_green(self):
        self.assertEqual(MAP_STYLE_VERSION, "blue-gold-high-contrast-v5")
        self.assertEqual(
            CHANGE_SCALE_COLORS,
            (
                (0.0, "#183153"),
                (0.25, "#4f76a8"),
                (0.4, "#a9bfdb"),
                (0.5, "#f4f4f1"),
                (0.58, "#fff0a6"),
                (0.65, "#e7c13f"),
                (0.72, "#ba8d00"),
                (0.8, "#8a6500"),
                (0.9, "#674a00"),
                (1.0, "#493400"),
            ),
        )

    def test_adaptive_scale_separates_values_despite_an_outlier(self):
        norm = AdaptiveDivergingNorm([1, 2, 3, 1000])

        self.assertAlmostEqual(float(norm(0)), 0.5)
        self.assertGreater(float(norm(3)) - float(norm(2)), 0.05)
        self.assertLess(float(norm(3)), float(norm(1000)))
        self.assertAlmostEqual(float(norm(-2)), 1 - float(norm(2)))

    def test_map_value_formatting_compacts_counts_without_losing_rate_precision(self):
        self.assertEqual(format_map_value(7_791_819, 0, compact=True), "+8M")
        self.assertEqual(format_map_value(-958_484, 0, compact=True), "−958K")
        self.assertEqual(format_map_value(12.34, 2, compact=True), "+12.34")
        self.assertEqual(format_map_value(128, 0, compact=False), "+128")

    def test_style_markers_are_stored_in_cache_not_beside_outputs(self):
        marker = DummyRetriever._style_marker_path(
            "outputs/North America/1990/2024/Population, total.png"
        )

        self.assertEqual(
            marker,
            "data/cache/styles/North America/1990/2024/Population, total.png.style".replace("/", os.sep),
        )

    def test_apply_diff_supports_all_exact_and_adjacent_endpoint_combinations(self):
        cases = {
            "both exact": (1990, 2020),
            "adjacent start": (1991, 2020),
            "adjacent end": (1990, 2019),
            "both adjacent": (1991, 2019),
        }
        region = SimpleNamespace(
            countries=[Country.UNITED_STATES, Country.CANADA],
            iso3_list=["USA", "CAN"],
        )

        for label, (canada_start, canada_end) in cases.items():
            with self.subTest(label=label):
                data = pd.DataFrame([
                    {"iso_a3": "USA", "year": 1990, "value": 10.0},
                    {"iso_a3": "USA", "year": 2020, "value": 20.0},
                    {"iso_a3": "CAN", "year": canada_start, "value": 100.0},
                    {"iso_a3": "CAN", "year": canada_end, "value": 250.0},
                ])

                result, year_from, year_to = DummyRetriever().apply_diff(
                    data=data,
                    data_column="value",
                    region=region,
                )
                canada = result.set_index("iso_a3").loc["CAN"]

                self.assertEqual((year_from, year_to), (1990, 2020))
                self.assertEqual(canada["1990_value"], 100.0)
                self.assertEqual(canada["2020_value"], 250.0)
                self.assertEqual(canada["data"], 150.0)

    def test_year_selection_does_not_treat_duplicate_rows_as_endpoint_coverage(self):
        region = SimpleNamespace(countries=[Country.UNITED_STATES, Country.CANADA])
        data = pd.DataFrame([
            {"iso_a3": "USA", "year": 1990, "value": 10.0},
            {"iso_a3": "USA", "year": 1990, "value": 10.0},
            {"iso_a3": "CAN", "year": 1990, "value": 20.0},
            {"iso_a3": "CAN", "year": 2019, "value": 30.0},
        ])

        retriever = DummyRetriever()
        retriever.max_year_range = [2019, 2022]
        years = retriever.good_years(
            data=data,
            data_column="value",
            region=region,
        )

        self.assertEqual(years, (1990, 2019))

    def test_year_selection_prefers_exact_year_over_later_adjacent_target(self):
        region = SimpleNamespace(countries=[Country.UNITED_STATES, Country.CANADA])
        data = pd.DataFrame([
            {"iso_a3": "USA", "year": 1990, "value": 10.0},
            {"iso_a3": "CAN", "year": 1990, "value": 20.0},
            {"iso_a3": "USA", "year": 2024, "value": 30.0},
            {"iso_a3": "CAN", "year": 2024, "value": 40.0},
        ])

        retriever = DummyRetriever()
        retriever.max_year_range = [2019, 2026]
        years = retriever.good_years(
            data=data,
            data_column="value",
            region=region,
        )

        self.assertEqual(years, (1990, 2024))

    def test_world_uses_geometry_centroids_for_every_country_label(self):
        self.assertTrue(all(country.label_coords(Map.WORLD) == (None, None)
                            for country in Map.WORLD.countries))

    def test_africa_membership_excludes_american_countries_and_includes_comoros(self):
        self.assertIn(Country.COMOROS, Map.AFRICA.countries)
        self.assertNotIn(Country.COSTA_RICA, Map.AFRICA.countries)
        self.assertNotIn(Country.ECUADOR, Map.AFRICA.countries)


if __name__ == "__main__":
    unittest.main()
