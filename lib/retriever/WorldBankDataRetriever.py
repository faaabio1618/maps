import json
import os
import time
from glob import glob

import pandas as pd
import requests
from pandas_datareader import wb
from pandas_datareader._utils import RemoteDataError
from requests.exceptions import RequestException

from lib.Country import names_to_iso3
from lib.retriever.AbstractDataRetriever import AbstractDataRetriever, LATEST_COMPLETE_YEAR

with open('data/indicators.json', encoding="utf-8") as f:
    indicators = json.load(f)[1]

dict_indicators = {ind["id"]: ind for ind in indicators}


class WorldBankDataRetriever(AbstractDataRetriever):

    def __init__(self, indicator, *, keep_unit=False, min_year_range=None, max_year_range=None, round=0,
                 show_final=True,
                 unit=None,
                 alternative_name=None,
                 max_retries=3,
                 retry_backoff_seconds=1,
                 country_batch_size=5,
                 fallback_to_dbnomics=True):
        if not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer")
        if retry_backoff_seconds < 0:
            raise ValueError("retry_backoff_seconds must be non-negative")
        if (
            not isinstance(country_batch_size, int)
            or isinstance(country_batch_size, bool)
            or country_batch_size < 1
        ):
            raise ValueError("country_batch_size must be a positive integer")
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
            max_year_range=max_year_range or [2019, LATEST_COMPLETE_YEAR],
            show_final=show_final,
            unit=unit,
            description=indicator_.get("sourceNote", ""),
            round=round)
        self.indicator = indicator
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.country_batch_size = country_batch_size
        self.fallback_to_dbnomics = fallback_to_dbnomics

    def retrieve(self, region):
        return self._retrieve_wb(region)

    def _retrieve_wb(self, region):
        cache_directory = f"./data/cache/{region.name}"
        cachefile = (
            f"{cache_directory}/wb_{self.indicator}"
            f"_through_{self.max_year_range[-1]}.csv"
        )
        if os.path.exists(cachefile):
            wb_data = pd.read_csv(cachefile)
        else:
            covering_cachefile = self._find_covering_cachefile(cache_directory)
            if covering_cachefile:
                wb_data = pd.read_csv(covering_cachefile)
            else:
                legacy_cachefile = f"{cache_directory}/wb_{self.indicator}.csv"
                legacy_data = (
                    pd.read_csv(legacy_cachefile)
                    if os.path.exists(legacy_cachefile)
                    else None
                )
                downloaded_data = self._download_wb(region)
                wb_data = self._merge_download_with_legacy_cache(
                    downloaded_data,
                    legacy_data,
                )
                os.makedirs(os.path.dirname(cachefile), exist_ok=True)
                wb_data.to_csv(cachefile)
        data = self._flatten_wb_data(wb_data)
        # Mirrors and older cache files can represent missing observations as
        # strings such as "NA". Normalize at the cache boundary so plotting
        # arithmetic always receives numeric values.
        data[self.indicator] = pd.to_numeric(data[self.indicator], errors='coerce')
        data['iso_a3'] = data['country'].map(names_to_iso3)
        data['year'] = data['year'].astype(int)
        data = data[data['year'].between(self.min_year_range[0], self.max_year_range[-1])]
        data = data.drop_duplicates(subset=['iso_a3', 'year'], keep='last')
        data.columns = ['country', 'year', self.indicator, 'iso_a3']
        return data, self.indicator

    def _find_covering_cachefile(self, cache_directory):
        filename_prefix = f"wb_{self.indicator}_through_"
        candidates = []
        for filename in glob(f"{cache_directory}/{filename_prefix}*.csv"):
            basename = os.path.basename(filename)
            try:
                cached_through_year = int(basename[len(filename_prefix):-len('.csv')])
            except ValueError:
                continue
            if cached_through_year >= self.max_year_range[-1]:
                candidates.append((cached_through_year, filename))
        return min(candidates)[1] if candidates else None

    def _flatten_wb_data(self, data):
        data = data.reset_index()
        return data[['country', 'year', self.indicator]].copy()

    def _merge_download_with_legacy_cache(self, downloaded_data, legacy_data):
        downloaded = self._flatten_wb_data(downloaded_data)
        if legacy_data is None:
            return downloaded.set_index(['country', 'year'])

        legacy = self._flatten_wb_data(legacy_data)
        merged = pd.concat([legacy, downloaded], ignore_index=True)
        merged[self.indicator] = pd.to_numeric(merged[self.indicator], errors='coerce')
        merged = merged.dropna(subset=[self.indicator])
        merged = merged.drop_duplicates(subset=['country', 'year'], keep='last')
        return merged.set_index(['country', 'year']).sort_index()

    def _download_wb(self, region):
        countries = [country for country in region.countries if not country.is_territory]
        country_codes = [country.iso2 for country in countries]
        # pandas_datareader hardcodes per_page=25,000 and does not follow
        # pagination links, so reducing per_page would silently lose rows.
        # Country batches reduce each response without truncating the result.
        country_batches = [
            country_codes[start:start + self.country_batch_size]
            for start in range(0, len(country_codes), self.country_batch_size)
        ]
        try:
            batch_results = [
                self._download_country_batch(batch, batch_number, len(country_batches))
                for batch_number, batch in enumerate(country_batches, start=1)
            ]
        except (RequestException, RemoteDataError) as error:
            if not self.fallback_to_dbnomics:
                raise
            reason = "blocked" if self._is_world_bank_waf_block(error) else "unavailable"
            print(f"World Bank is {reason}; using the DBnomics World Bank mirror for {self.indicator}.")
            return self._download_dbnomics(countries)
        if len(batch_results) == 1:
            return batch_results[0]
        return pd.concat(batch_results)

    def _download_country_batch(self, countries, batch_number, batch_count):
        for retry_number in range(self.max_retries + 1):
            try:
                return wb.download(
                    indicator=self.indicator,
                    country=countries,
                    start=self.min_year_range[0],
                    end=self.max_year_range[-1]
                )
            except (RequestException, RemoteDataError) as error:
                if isinstance(error, RemoteDataError) and self._is_world_bank_waf_block(error):
                    raise
                if retry_number == self.max_retries:
                    raise
                delay = self.retry_backoff_seconds * (2 ** retry_number)
                print(
                    f"World Bank download for {self.indicator} "
                    f"(country batch {batch_number}/{batch_count}) failed: "
                    f"{self._concise_error(error)}. "
                    f"Retrying in {delay} seconds "
                    f"({retry_number + 1}/{self.max_retries})..."
                )
                time.sleep(delay)

    @staticmethod
    def _is_world_bank_waf_block(error):
        message = str(error).lower()
        return "waf-block.html" in message or "5xx error page" in message

    @staticmethod
    def _concise_error(error):
        message = str(error).split("Response Text:", maxsplit=1)[0].strip()
        return " ".join(message.split())

    def _download_dbnomics(self, countries):
        records = []
        for country in countries:
            series_code = f"A-{self.indicator}-{country.iso3}"
            response = requests.get(
                f"https://api.db.nomics.world/v22/series/WB/WDI/{series_code}",
                params={"observations": 1, "metadata": "false"},
                timeout=30,
            )
            response.raise_for_status()
            documents = response.json().get("series", {}).get("docs", [])
            if not documents:
                continue
            document = documents[0]
            for period, value in zip(document.get("period", []), document.get("value", [])):
                year = int(period)
                if self.min_year_range[0] <= year <= self.max_year_range[-1]:
                    records.append({
                        "country": country.name,
                        "year": str(year),
                        self.indicator: value,
                    })

        if not records:
            raise RemoteDataError(
                f"DBnomics returned no data for World Bank indicator {self.indicator}"
            )
        return pd.DataFrame.from_records(records).set_index(["country", "year"])
