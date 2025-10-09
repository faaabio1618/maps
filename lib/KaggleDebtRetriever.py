from lib.Country import Country, names_to_iso3
from lib.KaggleRetriever import KaggleRetriever


class KaggleDebtRetriever(KaggleRetriever):

    def __init__(self):
        super().__init__(
            keep_unit=True,
            data_name="Debt as % GDP",
            source="https://www.kaggle.com/datasets/justin2028/debt-per-gdp-by-country",
            min_year_range=[1990, 1995],
            unit='% of GDP',
            round=2,
            show_final=True,
            description="The Global Debt Database (GDD) is the outcome of an extensive investigative process initiated with the October 2016 Fiscal Monitor. This dataset encapsulates the total gross debt of the nonfinancial sector (both private and public) for an unbalanced panel of 190 advanced economies, emerging market economies, and low-income countries, with records dating back to 1950. The Global Debt Dataset aggregates information from diverse sources to offer a comprehensive view of both public and private debt metrics. It includes data on government debt, corporate debt, household debt, and external debt, enabling users to delve into trends, patterns, and interrelationships among different debt categories.",
            kaggle_handle="sazidthe1/global-debt-data",

            file_names=["central_government_debt.csv"],
            max_year_range=[2020, 2023]
        )

    def retrieve(self, region):
        data = self._retrieve_kaggle(region)["central_government_debt.csv"]
        data["iso_a3"] = data["country_name"].map(lambda c: names_to_iso3(c))
        # drop countries with no iso3
        data = data[data["iso_a3"].notna()]
        data = data.drop(columns=["Unnamed: 0", "country_name", "indicator_name"])
        data = data.melt(id_vars=["iso_a3"], var_name="year", value_name="debt")
        data["year"] = data["year"].astype(int)
        data["debt"] = data["debt"].astype(float)
        return data, "debt"
