import unittest
from types import SimpleNamespace
from unittest.mock import Mock, mock_open, patch

from requests.exceptions import ReadTimeout

from lib.Map import Map
from lib.retriever.AbstractDataRetriever import NoComparableDataError


class MapBatchResilienceTests(unittest.TestCase):
    @patch("lib.Map.shutil.copy")
    @patch("lib.Map.os.makedirs")
    def test_transient_download_failure_is_skipped_and_batch_continues(self, makedirs, copy):
        failed = SimpleNamespace(
            data_name="Intentional homicides",
            indicator="VC.IHR.PSRC.P5",
            plot=Mock(side_effect=ReadTimeout("World Bank timed out")),
        )
        successful = SimpleNamespace(
            data_name="Population",
            plot=Mock(return_value="generated.png"),
        )
        region = SimpleNamespace(
            name="North America",
            retrievers=[failed, successful],
        )

        opened_log = mock_open()
        with patch("builtins.open", opened_log), patch("builtins.print") as print_message:
            Map.to_reddit(region)

        failed.plot.assert_called_once_with(region=region)
        successful.plot.assert_called_once_with(region=region)
        copy.assert_called_once_with(
            "generated.png",
            "data/reddit/North America/02.Population.png",
        )
        opened_log.assert_called_once_with(
            "data/reddit/North America/errors.log",
            "a",
            encoding="utf-8",
        )
        self.assertIn("VC.IHR.PSRC.P5", print_message.call_args.args[0])
        self.assertIn("Skipping", print_message.call_args.args[0])
        self.assertIs(print_message.call_args.kwargs["file"], opened_log())

    @patch("lib.Map.shutil.copy")
    @patch("lib.Map.os.makedirs")
    def test_non_transient_plot_failure_still_stops_the_batch(self, makedirs, copy):
        failed = SimpleNamespace(
            data_name="Broken map",
            plot=Mock(side_effect=ValueError("invalid data")),
        )
        region = SimpleNamespace(name="Test", retrievers=[failed])

        with self.assertRaises(ValueError):
            Map.to_reddit(region)

        copy.assert_not_called()

    @patch("lib.Map.shutil.copy")
    @patch("lib.Map.os.makedirs")
    def test_no_comparable_data_is_logged_and_batch_continues(self, makedirs, copy):
        failed = SimpleNamespace(
            data_name="Sparse indicator",
            indicator="TEST.SPARSE",
            plot=Mock(side_effect=NoComparableDataError("no comparable years")),
        )
        successful = SimpleNamespace(
            data_name="Population",
            plot=Mock(return_value="generated.png"),
        )
        region = SimpleNamespace(
            name="North America",
            retrievers=[failed, successful],
        )

        opened_log = mock_open()
        with patch("builtins.open", opened_log), patch("builtins.print") as print_message:
            Map.to_reddit(region)

        successful.plot.assert_called_once_with(region=region)
        copy.assert_called_once()
        self.assertIn("no comparable years", print_message.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
