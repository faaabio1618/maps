import os
from enum import Enum
import shutil

import numpy as np

from lib.ComposedDataRetriever import ComposedDataRetriever
from lib.Country import Country
from lib.CumulativeInflation import CumulativeInflation
from lib.EconomicFreedomRetriever import EconomicFreedomRetriever
from lib.KaggleAverageTemperatureRetriever import KaggleAverageTemperatureRetriever
from lib.KaggleDebtRetriever import KaggleDebtRetriever
from lib.KaggleTourismRetriever import KaggleTourismRetriever
from lib.WorldBankDataRetriever import WorldBankDataRetriever, dict_indicators

pyhsicians = WorldBankDataRetriever("SH.MED.PHYS.ZS", alternative_name="Physicians per 1000 people")
gdp_per_capita = WorldBankDataRetriever("NY.GDP.PCAP.CD")
gdp_per_employed = WorldBankDataRetriever("SL.GDP.PCAP.EM.KD", alternative_name="GDP per person employed (PPP $)")
refugee_by_population = ComposedDataRetriever(data_name="Refugees per 1000 people",
                                              retriever_1=WorldBankDataRetriever("SM.POP.RHCR.EA", keep_unit=True),
                                              retriever_2=WorldBankDataRetriever("SP.POP.TOTL"), round=1, is_rate=True,
                                              unit="per 1000 people",
                                              description=dict_indicators["SM.POP.RHCR.EA"].get("sourceNote"),
                                              function=lambda x, y: x / y * 1000 if not np.isnan(x) and not np.isnan(
                                                  y) and y != 0 else np.nan, )
alchool = WorldBankDataRetriever("SH.ALC.PCAP.LI", min_year_range=[2000, 2001], unit="litre of pure alcohol per year")
inflation = CumulativeInflation()
debtRetriever = KaggleDebtRetriever()
fossil_fuel = WorldBankDataRetriever("EG.USE.COMM.FO.ZS", keep_unit=True, round=1)
energy_use_per_capita = WorldBankDataRetriever("EG.USE.PCAP.KG.OE")
labor_force = WorldBankDataRetriever("SL.TLF.TOTL.IN")
birth_rate = WorldBankDataRetriever("SP.DYN.CBRT.IN", keep_unit=True)
life_expectancy = WorldBankDataRetriever("SP.DYN.LE00.IN", keep_unit=True)
popover65 = WorldBankDataRetriever("SP.POP.65UP.TO.ZS", keep_unit=True, round=1)
population = WorldBankDataRetriever("SP.POP.TOTL")
temperature_retriever = KaggleAverageTemperatureRetriever()
tourism_retriever = KaggleTourismRetriever()
freedom_retriever = EconomicFreedomRetriever()
homicides = WorldBankDataRetriever("VC.IHR.PSRC.P5", min_year_range=[1990, 2002])
militar_expenses = WorldBankDataRetriever("MS.MIL.XPND.GD.ZS", keep_unit=True, round=1)


class Map(Enum):
    ASIA = {
        "retrievers": [
            population,
            gdp_per_capita,
            life_expectancy,
            # fossil_fuel,
            energy_use_per_capita,
            militar_expenses,
            debtRetriever,
            freedom_retriever,
            alchool,
            labor_force,
            gdp_per_employed,
            pyhsicians,
            birth_rate,
            popover65,
            homicides,
            temperature_retriever,
            tourism_retriever,
            refugee_by_population,
        ],
        "name": "Asia",
        "crs": "+proj=lcc +lat_1=15 +lat_2=45 +lat_0=30 +lon_0=100 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs",
        "legends": {
            "rank": "left",
            "description": [(0.035, 0.0), "left", "bottom"],
            "source": [(1.0, 0.0), "right", "bottom"],
            "attribution": [(1.0, 1.0), "right", "top"]
        },

        "map_limits": {
            "minx": -6000000,
            "maxx": 4000000,
            "miny": -4500000,
            "maxy": 3500000
        },
        "countries": [
            Country.AFGHANISTAN,
            Country.BAHRAIN,
            Country.BANGLADESH,
            Country.BHUTAN,
            Country.BRUNEI,
            Country.AZERBAIJAN,
            Country.GEORGIA,
            Country.ARMENIA,
            Country.CAMBODIA,
            Country.EAST_TIMOR,
            Country.INDIA,
            Country.INDONESIA,
            Country.IRAN,
            Country.IRAQ,
            Country.ISRAEL,
            Country.JAPAN,
            Country.JORDAN,
            Country.KUWAIT,
            Country.KAZAKHSTAN,
            Country.KYRGYZSTAN,
            Country.LAOS,
            Country.LEBANON,
            Country.MALAYSIA,
            Country.MALDIVES,
            Country.MONGOLIA,
            Country.MYANMAR,
            Country.NEPAL,
            Country.NORTH_KOREA,
            Country.OMAN,
            Country.PAKISTAN,
            Country.PALESTINE,
            Country.PHILIPPINES,
            Country.QATAR,
            Country.SAUDI_ARABIA,
            Country.SINGAPORE,
            Country.SOUTH_KOREA,
            Country.SRI_LANKA,
            Country.SYRIA,
            Country.TAJIKISTAN,
            Country.THAILAND,
            Country.TURKEY,
            Country.TURKMENISTAN,
            Country.UNITED_ARAB_EMIRATES,
            Country.UZBEKISTAN,
            Country.VIETNAM,
            Country.YEMEN,
            Country.CHINA,
            Country.TAIWAN,
            Country.RUSSIA,
        ]}

    EUROPE = {
        "name": "Europe",
        "retrievers": [
            inflation,
            debtRetriever,
            fossil_fuel,
            energy_use_per_capita,
            WorldBankDataRetriever("GC.TAX.TOTL.GD.ZS", keep_unit=True, round=1),
            militar_expenses,
            WorldBankDataRetriever("NY.ADJ.NNTY.PC.KD"),
            gdp_per_capita,
            alchool,
            pyhsicians,
            # arms,
            gdp_per_employed,
            labor_force,
            WorldBankDataRetriever("SM.POP.RHCR.EA", keep_unit=True),
            birth_rate,
            life_expectancy,
            popover65,
            WorldBankDataRetriever("SP.POP.TOTL", show_final=True),
            WorldBankDataRetriever("VC.IHR.PSRC.P5"),
            temperature_retriever,
            tourism_retriever,
            freedom_retriever,
            refugee_by_population,
        ],
        "crs": "3035",
        "legends": {
            "rank": "right",
            "description": [(1, 0.01), "right", "bottom"],
            "source": [(0.01, 0.01), "left", "bottom"],
            "attribution": [(0.995, 0.994), "right", "top"]
        },
        "map_limits": {
            "minx": 2620000,
            "maxx": 7600000,
            "miny": 1390000,
            "maxy": 5430000
        },
        "countries": [
            Country.ALBANIA,
            Country.ANDORRA,
            Country.AZERBAIJAN,
            Country.ARMENIA,
            Country.AUSTRIA,
            Country.BELGIUM,
            Country.BELARUS,
            Country.BOSNIA_HERZEGOVINA,
            Country.BULGARIA,
            Country.CYPRUS,
            Country.CZECHIA,
            Country.CROATIA,
            Country.DENMARK,
            Country.ESTONIA,
            Country.FINLAND,
            Country.FRANCE,
            Country.GEORGIA,
            Country.GERMANY,
            Country.GREECE,
            Country.HUNGARY,
            Country.KAZAKHSTAN,
            Country.KOSOVO,
            Country.ICELAND,
            Country.IRELAND,
            Country.ITALY,
            Country.LATVIA,
            Country.LIECHTENSTEIN,
            Country.LITHUANIA,
            Country.LUXEMBOURG,
            Country.MOLDOVA,
            Country.NORTH_MACEDONIA,
            Country.MALTA,
            Country.MONACO,
            Country.MONTENEGRO,
            Country.NETHERLANDS,
            Country.NORWAY,
            Country.POLAND,
            Country.PORTUGAL,
            Country.ROMANIA,
            Country.RUSSIA,
            Country.SAN_MARINO,
            Country.SERBIA,
            Country.SLOVAKIA,
            Country.SLOVENIA,
            Country.SPAIN,
            Country.SWEDEN,
            Country.SWITZERLAND,
            Country.TURKEY,
            Country.UKRAINE,
            Country.UNITED_KINGDOM
        ]
    }

    def __getitem__(self, item):
        return item

    @property
    def name(self):
        return self.value["name"]

    @property
    def map_limits(self):
        return self.value["map_limits"]

    @property
    def countries(self):
        return self.value["countries"]

    @property
    def iso3_list(self):
        return [country.iso3 for country in self.countries]

    @property
    def iso2_list(self):
        return [country.iso2 for country in self.countries]

    @property
    def crs(self):
        return self.value["crs"]

    @property
    def description_position(self):
        return self.value["legends"]["description"]

    @property
    def source_position(self):
        return self.value["legends"]["source"]

    @property
    def attribution_position(self):
        return self.value["legends"]["attribution"]

    @property
    def retrievers(self):
        return self.value["retrievers"]

    @property
    def rank_position(self):
        return self.value["legends"]["rank"]

    def to_reddit(self):
        reddit_folder = f"data/reddit/{self.name}"
        os.makedirs(reddit_folder, exist_ok=True)
        for i, ret in enumerate(self.retrievers):
            filename = ret.plot(region=self)
            padded_i = str(i+1).zfill(2)
            shutil.copy(filename, f"{reddit_folder}/{padded_i}.{ret.data_name}.png")
