import pandas as pd

from lib.retriever.AbstractDataRetriever import AbstractDataRetriever


class AlcoholRetriever(AbstractDataRetriever):

    def __init__(self):
        super().__init__(
            description="Total APC is defined as the total (sum of three-year average recorded and three-year average unrecorded APC, adjusted for three-year average tourist consumption) amount of alcohol consumed per adult (15+ years) over a calendar year, in litres of pure alcohol. Recorded alcohol consumption refers to official statistics (production, import, export, and sales or taxation data), while the unrecorded alcohol consumption refers to alcohol which is not taxed and is outside the usual system of governmental control. Tourist consumption takes into account tourists visiting the country and inhabitants visiting other countries. Positive figures denote alcohol consumption of outbound tourists being greater than alcohol consumption by inbound tourists, negative numbers the opposite. Tourist consumption is based on UN tourist statistics.",
            source="https://www.who.int/data/gho/data/indicators",
            round=0,
            show_final=True,
            max_year_range=[2021,2021],
            min_year_range=[2000,2000],
            data_name="Alcohol, total per capita (15+) consumption",
            unit="litre of pure alcohol"
        )

    def retrieve(self, region):
        csv_path = "data/alcohol.csv"
        data = pd.read_csv(csv_path)
        data["iso_a3"] = data["SpatialDimValueCode"]
        data = data[data['iso_a3'].isin([country.iso3 for country in region.countries])]
        data["year"] = data["Period"].astype(int)
        data["litres"] = data["FactValueNumeric"].astype(float)
        data = data[["iso_a3", "year", "litres"]]
        return data, "litres"
