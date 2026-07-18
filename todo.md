# Code review TODO

Review scope: current working tree, including the uncommitted changes in `main.py` and `lib/Map.py`. All project Python files and every tracked file under `data/` were read end-to-end; generated cache/PNG files present during the review pass were also read and validated. The CSV files parsed with consistent row widths, `data/indicators.json` parsed successfully (29,201 indicators), and the generated PNGs decoded successfully.

## P0 — correctness

- [x] Fix the adjacent-year fallback in `AbstractDataRetriever.apply_diff()` (`lib/retriever/AbstractDataRetriever.py:349-415`). Endpoint rows are now selected explicitly before their years are normalized, with regression coverage for all four exact/adjacent combinations.

- [x] Make custom label coordinates CRS- and region-aware before using `Map.WORLD` (`lib/Map.py:63-87`, `lib/Country.py:1108-1218`). World maps now use each geometry's centroid instead of projected region-specific overrides.

- [x] Correct the Africa country list (`lib/Map.py:329-389`). Costa Rica and Ecuador were removed, and Comoros was added.

## P1 — broken or misleading features

- [ ] Stop swapping UN Statistics year ranges (`lib/retriever/UnStatRetriever.py:23-24`). Passing `min_year_range=[1990, 1995]` and `max_year_range=[2020, 2024]` currently stores them as `[2020, 2024]` and `[1990, 1995]`, making the retriever invalid as soon as it is enabled.

- [ ] Fix the import in `lib/retriever/KaggleArmsImport.py:2`. Importing this module raises `ModuleNotFoundError: No module named 'lib.KaggleRetriever'`; the implementation lives at `lib.retriever.KaggleRetriever`.

- [ ] Reset `partial_countries` for each calculation (`lib/retriever/AbstractDataRetriever.py:63, 349-361`). Retriever instances are global and shared by multiple regions in `lib/Map.py`, but this mutable list is never cleared. Running regions sequentially can mark later maps with stale parenthesized labels and the wrong adjacent-year note.

- [ ] Handle empty, all-missing, and all-zero datasets in plotting (`lib/retriever/AbstractDataRetriever.py:164-176, 257-272`). `nanmin`/`nanmax` and the ranks' `max()` fail on empty data, while an all-zero dataset builds `TwoSlopeNorm(vmin=0, vcenter=0.1, vmax=0)`, which raises because the bounds are not ascending. Add an explicit no-data path and a valid single-color/linear normalization for constant data.

- [ ] Remove the duplicate `gdp_per_capita` entry from `Map.WORLD.retrievers` (`lib/Map.py:67,70`). It currently creates the same GDP map twice and copies duplicate content into two numbered Reddit images.

- [ ] Correct the cumulative-inflation source URL (`lib/retriever/CumulativeInflation.py:14`). The code retrieves `FP.CPI.TOTL.ZG`, but the displayed source points to `SI.XPD.CHEX.GD.ZS`, a different indicator, so generated maps cite the wrong data page.

- [ ] Correct the unit for cumulative migration (`lib/retriever/CumulativeImmigration.py:15`). The retriever sums net migrant counts but declares the unit as `%`, causing the final-value legend to label counts as percentages.

- [ ] Honor caller-provided year ranges in `DebtRetrieval` (`lib/retriever/DebtRetriever.py:10-22, 38-41`). The constructor accepts custom ranges and passes them to the base class, but then hard-codes 1995 and 2024 and filters exclusively to those years.

## P2 — resilience and maintainability

- [ ] Make network retrieval fail safely (`lib/retriever/AbstractDataRetriever.py:76-82`, `lib/retriever/UnStatRetriever.py:41-53`). Add timeouts to every request, call `raise_for_status()`, validate downloaded GeoJSON/JSON before caching it, and avoid recursive retries on a bad response. A transient HTTP error can currently be saved as a map file and fail later with an unrelated parsing error.

- [ ] Replace bare `except:` blocks (`lib/Country.py:1279-1296`, `lib/retriever/KaggleRetriever.py:54-57`, `lib/retriever/WorldBankDataRetriever.py:25-28`) with the narrow exceptions that are expected. The current handlers also swallow interrupts and unrelated programming errors, which makes bad data and code defects look like normal fallbacks.

- [ ] Include the query shape in cache identity or validate cached coverage (`lib/retriever/WorldBankDataRetriever.py:48-58`, `lib/retriever/KaggleRetriever.py:46-60`). World Bank cache names omit requested years/countries, and Kaggle cache names omit the source filename. Changed ranges or multi-file datasets can silently reuse incomplete or incorrect cached data.

- [ ] Add automated tests before changing the data pipeline. Prioritize `good_years()`, adjacent-year selection, percentage-vs-unit differences, composed retrievers, region membership, country-name aliases, cache behavior, and constant/no-data plotting. There is currently no test suite, so the confirmed adjacent-year regression and invalid region membership are not detected automatically.

- [ ] Align documentation and dependencies with the code. `Readme.md` claims Python 3.8 support, but `list[Country]` syntax requires Python 3.9+, and it advertises SVG export/pip-installability that the repository does not implement. Also declare direct dependencies such as `requests` explicitly and pin or bound the currently unversioned packages in `requirements.txt` for reproducible installs.

- [ ] Replace the hard-coded batch selection in `main.py:8-15` with CLI options (region, retriever, force/dry-run). The current entry point always processes Americas and then World, which can perform many downloads and overwrite/copy a large set of generated images when the script is run accidentally.
