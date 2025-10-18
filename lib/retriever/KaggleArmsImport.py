from lib.Country import Country, names_to_iso3
from lib.KaggleRetriever import KaggleRetriever


class KaggleArmsImport(KaggleRetriever):

    def __init__(self):
        super().__init__(
            keep_unit=False,
            data_name="Number of arms imports",
            source="https://www.kaggle.com/datasets/justin2028/arms-imports-per-country",
            min_year_range=[1990, 1995],
            unit="Millions",
            max_year_range=[2019, 2020],
            show_final=True,
            description="All data are official figures from the Stockholm International Peace Research Institute",
            kaggle_handle="justin2028/arms-imports-per-country",
            file_names=["Arms Imports Per Country (1950-2020).csv"],
            round=0,

        )

    def retrieve(self, region):
        data = self._retrieve_kaggle(region)["Arms Imports Per Country (1950-2020).csv"]
        data["iso_a3"] = data["Country/Region/Group"].map(lambda c: names_to_iso3(c))
        data = data[data["iso_a3"].notna()]
        data = data.drop(columns=["Unnamed: 0", "Country/Region/Group", "Total"])
        data = data.melt(id_vars=["iso_a3"], var_name="year", value_name="arms_imports")
        data["year"] = data["year"].astype(int)
        data["arms_imports"] = data["arms_imports"].astype(float)
        return data, "arms_imports"