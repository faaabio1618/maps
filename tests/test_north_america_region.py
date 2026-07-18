import unittest
from pathlib import Path

from lib.Country import Country, names_to_iso3
from lib.Map import Map, migration, population


class NorthAmericaRegionTests(unittest.TestCase):
    EXPECTED_COUNTRIES = {
        Country.BAHAMAS,
        Country.BELIZE,
        Country.CANADA,
        Country.COSTA_RICA,
        Country.CUBA,
        Country.DOMINICAN_REPUBLIC,
        Country.EL_SALVADOR,
        Country.GUATEMALA,
        Country.HAITI,
        Country.HONDURAS,
        Country.JAMAICA,
        Country.MEXICO,
        Country.NICARAGUA,
        Country.PANAMA,
        Country.UNITED_STATES,
    }

    def test_region_excludes_requested_clustered_caribbean_states(self):
        self.assertEqual(len(Map.NORTH_AMERICA.countries), 15)
        self.assertEqual(set(Map.NORTH_AMERICA.countries), self.EXPECTED_COUNTRIES)
        self.assertNotIn(Country.BARBADOS, Map.NORTH_AMERICA.countries)
        self.assertNotIn(Country.TRINIDAD_TOBAGO, Map.NORTH_AMERICA.countries)

    def test_countries_below_mexico_use_smaller_font_without_new_displacements(self):
        smaller_label_countries = [
            Country.BAHAMAS,
            Country.BELIZE,
            Country.CUBA,
            Country.DOMINICAN_REPUBLIC,
            Country.GUATEMALA,
            Country.HAITI,
            Country.HONDURAS,
            Country.EL_SALVADOR,
            Country.JAMAICA,
            Country.NICARAGUA,
            Country.COSTA_RICA,
            Country.PANAMA,
        ]

        self.assertTrue(all(Map.NORTH_AMERICA.label_font_reduction(country) == 3
                            for country in smaller_label_countries))
        self.assertEqual(Map.NORTH_AMERICA.label_font_reduction(Country.MEXICO), 0)
        self.assertEqual(Map.NORTH_AMERICA.label_font_reduction(Country.UNITED_STATES), 0)
        self.assertEqual(Map.NORTH_AMERICA.label_font_reduction(Country.CANADA), 0)
        self.assertEqual(Country.HONDURAS.label_coords(Map.NORTH_AMERICA), (None, None))

    def test_description_and_credit_use_opposite_corners(self):
        self.assertEqual(Map.NORTH_AMERICA.description_position, [(0.01, 0.94), "left", "top"])
        self.assertFalse(Map.NORTH_AMERICA.description_follows_rank)
        self.assertEqual(Map.NORTH_AMERICA.attribution_position, [(0.995, 0.01), "right", "bottom"])

    def test_population_absolute_values_are_enabled_only_for_north_america(self):
        north_america_population = Map.NORTH_AMERICA.retrievers[0]

        self.assertEqual(north_america_population.indicator, "SP.POP.TOTL")
        self.assertTrue(north_america_population.show_final)
        self.assertFalse(population.show_final)
        self.assertIn("na-population-values", north_america_population.output_style_version)

    def test_net_migration_is_measured_in_people_not_percent(self):
        self.assertEqual(migration.unit, "people")

    def test_every_country_has_a_local_map(self):
        missing = [country.iso3 for country in Map.NORTH_AMERICA.countries
                   if not Path(f"maps/gadm41_{country.iso3}_0.json").exists()]
        self.assertEqual(missing, [])

    def test_world_bank_aliases_cover_abbreviated_saint_names(self):
        self.assertEqual(names_to_iso3("St. Kitts and Nevis"), "KNA")
        self.assertEqual(names_to_iso3("St. Vincent and the Grenadines"), "VCT")

    def test_global_hong_kong_row_has_an_iso3_alias(self):
        self.assertEqual(names_to_iso3("Hong Kong SAR"), "HKG")
        self.assertEqual(names_to_iso3("Hong Kong SAR, China"), "HKG")


if __name__ == "__main__":
    unittest.main()
