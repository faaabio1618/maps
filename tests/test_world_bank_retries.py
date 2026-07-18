import unittest
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

import pandas as pd
from pandas_datareader._utils import RemoteDataError
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import ReadTimeout

from lib.Country import Country
from lib.retriever.AbstractDataRetriever import CURRENT_YEAR, LATEST_COMPLETE_YEAR
from lib.retriever.WorldBankDataRetriever import WorldBankDataRetriever


class WorldBankRetryTests(unittest.TestCase):
    def setUp(self):
        self.region = SimpleNamespace(
            name="Test Region",
            countries=[Country.UNITED_STATES],
        )

    def test_default_download_range_excludes_the_current_year(self):
        retriever = WorldBankDataRetriever("SP.POP.TOTL")

        self.assertEqual(LATEST_COMPLETE_YEAR, CURRENT_YEAR - 1)
        self.assertEqual(retriever.max_year_range, [2019, LATEST_COMPLETE_YEAR])

    @patch("lib.retriever.WorldBankDataRetriever.time.sleep")
    @patch("lib.retriever.WorldBankDataRetriever.wb.download")
    def test_read_timeout_is_retried_until_download_succeeds(self, download, sleep):
        expected = pd.DataFrame({"SP.POP.TOTL": [1]})
        download.side_effect = [
            ReadTimeout("first timeout"),
            ReadTimeout("second timeout"),
            expected,
        ]
        retriever = WorldBankDataRetriever("SP.POP.TOTL")

        result = retriever._download_wb(self.region)

        self.assertIs(result, expected)
        self.assertEqual(download.call_count, 3)
        self.assertEqual(sleep.call_args_list, [call(1), call(2)])

    @patch("lib.retriever.WorldBankDataRetriever.time.sleep")
    @patch("lib.retriever.WorldBankDataRetriever.wb.download")
    def test_last_timeout_is_raised_after_three_retries(self, download, sleep):
        download.side_effect = ReadTimeout("still unavailable")
        retriever = WorldBankDataRetriever(
            "SP.POP.TOTL",
            max_retries=3,
            fallback_to_dbnomics=False,
        )

        with self.assertRaises(ReadTimeout):
            retriever._download_wb(self.region)

        self.assertEqual(download.call_count, 4)
        self.assertEqual(sleep.call_args_list, [call(1), call(2), call(4)])

    @patch("lib.retriever.WorldBankDataRetriever.time.sleep")
    @patch("lib.retriever.WorldBankDataRetriever.wb.download")
    def test_connection_errors_are_retried(self, download, sleep):
        expected = pd.DataFrame({"SP.POP.TOTL": [1]})
        download.side_effect = [RequestsConnectionError("disconnected"), expected]
        retriever = WorldBankDataRetriever(
            "SP.POP.TOTL",
            max_retries=1,
            retry_backoff_seconds=0,
        )

        result = retriever._download_wb(self.region)

        self.assertIs(result, expected)
        self.assertEqual(download.call_count, 2)
        sleep.assert_called_once_with(0)

    @patch("lib.retriever.WorldBankDataRetriever.time.sleep")
    @patch("lib.retriever.WorldBankDataRetriever.wb.download")
    def test_non_transient_errors_are_not_retried(self, download, sleep):
        download.side_effect = ValueError("invalid request")
        retriever = WorldBankDataRetriever("SP.POP.TOTL")

        with self.assertRaises(ValueError):
            retriever._download_wb(self.region)

        download.assert_called_once()
        sleep.assert_not_called()

    @patch("lib.retriever.WorldBankDataRetriever.pd.read_csv")
    @patch("lib.retriever.WorldBankDataRetriever.os.path.exists", return_value=True)
    def test_cached_text_values_are_normalized_to_numbers(self, exists, read_csv):
        read_csv.return_value = pd.DataFrame({
            "country": ["United States", "Canada"],
            "year": [2024, 2024],
            "SP.POP.TOTL": ["340000000", "NA"],
        })
        retriever = WorldBankDataRetriever("SP.POP.TOTL")

        data, indicator = retriever.retrieve(self.region)

        self.assertEqual(indicator, "SP.POP.TOTL")
        self.assertEqual(data.loc[0, indicator], 340000000)
        self.assertTrue(pd.isna(data.loc[1, indicator]))
        read_csv.assert_called_once_with(
            f"./data/cache/Test Region/wb_SP.POP.TOTL_through_{LATEST_COMPLETE_YEAR}.csv"
        )

    def test_new_download_keeps_newer_values_from_the_legacy_cache(self):
        retriever = WorldBankDataRetriever("SP.POP.TOTL")
        legacy = pd.DataFrame({
            "country": ["Canada", "Canada"],
            "year": [2023, 2024],
            "SP.POP.TOTL": [10, 20],
        })
        downloaded = pd.DataFrame({
            "SP.POP.TOTL": [11],
        }, index=pd.MultiIndex.from_tuples(
            [("Canada", 2023)],
            names=["country", "year"],
        ))

        merged = retriever._merge_download_with_legacy_cache(downloaded, legacy)

        self.assertEqual(merged.loc[("Canada", 2023), "SP.POP.TOTL"], 11)
        self.assertEqual(merged.loc[("Canada", 2024), "SP.POP.TOTL"], 20)

    @patch("lib.retriever.WorldBankDataRetriever.glob")
    @patch("lib.retriever.WorldBankDataRetriever.pd.read_csv")
    @patch("lib.retriever.WorldBankDataRetriever.os.path.exists", return_value=False)
    def test_newer_cache_is_reused_but_current_year_is_excluded(self, exists, read_csv, find):
        newer_cache = f"./data/cache/Test Region/wb_SP.POP.TOTL_through_{CURRENT_YEAR}.csv"
        find.return_value = [newer_cache]
        read_csv.return_value = pd.DataFrame({
            "country": ["United States", "United States"],
            "year": [LATEST_COMPLETE_YEAR, CURRENT_YEAR],
            "SP.POP.TOTL": [340000000, 341000000],
        })
        retriever = WorldBankDataRetriever("SP.POP.TOTL")

        data, _ = retriever.retrieve(self.region)

        read_csv.assert_called_once_with(newer_cache)
        self.assertEqual(data["year"].tolist(), [LATEST_COMPLETE_YEAR])

    @patch("lib.retriever.WorldBankDataRetriever.wb.download")
    def test_countries_are_downloaded_in_small_batches_and_combined(self, download):
        countries = [
            SimpleNamespace(iso2=iso2, is_territory=False)
            for iso2 in ["US", "CA", "MX", "BZ", "CR", "CU", "DO"]
        ]
        region = SimpleNamespace(countries=countries)
        download.side_effect = [
            pd.DataFrame({"SP.POP.TOTL": [batch_number]})
            for batch_number in range(3)
        ]
        retriever = WorldBankDataRetriever("SP.POP.TOTL", country_batch_size=3)

        result = retriever._download_wb(region)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            [request.kwargs["country"] for request in download.call_args_list],
            [["US", "CA", "MX"], ["BZ", "CR", "CU"], ["DO"]],
        )

    @patch("lib.retriever.WorldBankDataRetriever.time.sleep")
    @patch("lib.retriever.WorldBankDataRetriever.wb.download")
    def test_world_bank_http_errors_are_retried(self, download, sleep):
        expected = pd.DataFrame({"SP.POP.TOTL": [1]})
        download.side_effect = [RemoteDataError("service unavailable"), expected]
        retriever = WorldBankDataRetriever("SP.POP.TOTL", retry_backoff_seconds=0)

        result = retriever._download_wb(self.region)

        self.assertIs(result, expected)
        self.assertEqual(download.call_count, 2)
        sleep.assert_called_once_with(0)

    @patch("lib.retriever.WorldBankDataRetriever.requests.get")
    @patch("lib.retriever.WorldBankDataRetriever.time.sleep")
    @patch("lib.retriever.WorldBankDataRetriever.wb.download")
    def test_world_bank_waf_block_uses_dbnomics_fallback(self, download, sleep, get):
        download.side_effect = RemoteDataError(
            "Unable to read URL\nResponse Text:\n<title>5xx Error Page</title>"
        )
        response = Mock()
        response.json.return_value = {
            "series": {
                "docs": [{
                    "period": ["1989", "1990", "2024", "2025"],
                    "value": [1, 2, 3, 4],
                }]
            }
        }
        get.return_value = response
        retriever = WorldBankDataRetriever("SP.POP.TOTL")

        result = retriever._download_wb(self.region)

        download.assert_called_once()
        sleep.assert_not_called()
        get.assert_called_once_with(
            "https://api.db.nomics.world/v22/series/WB/WDI/A-SP.POP.TOTL-USA",
            params={"observations": 1, "metadata": "false"},
            timeout=30,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(
            result.index.tolist(),
            [("United States", "1990"), ("United States", "2024"), ("United States", "2025")],
        )
        self.assertEqual(result["SP.POP.TOTL"].tolist(), [2, 3, 4])


if __name__ == "__main__":
    unittest.main()
