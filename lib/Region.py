from enum import Enum

from lib.Country import Country
from lib.Retrievers import DebtRetrieval
from lib.WorldBankDataRetriever import WorldBankDataRetriever


class Region(Enum):
    ASIA = {
        "retrievers" : [
            DebtRetrieval("Debt as % of GDP", is_rate=True),
            WorldBankDataRetriever("EG.USE.COMM.FO.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("EG.USE.PCAP.KG.OE"),
            WorldBankDataRetriever("GC.TAX.TOTL.GD.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("MS.MIL.XPND.GD.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("NY.ADJ.NNTY.PC.KD"),
            WorldBankDataRetriever("NY.GDP.PCAP.KN"),
            WorldBankDataRetriever("SH.ALC.PCAP.LI", min_year_range=[2000, 2001]),
            WorldBankDataRetriever("SH.MED.PHYS.ZS"),
            WorldBankDataRetriever("SL.GDP.PCAP.EM.KD"),
            WorldBankDataRetriever("SL.TLF.TOTL.IN"),
            WorldBankDataRetriever("SM.POP.RHCR.EA", is_rate=True),
            WorldBankDataRetriever("SP.DYN.CBRT.IN", is_rate=True),
            WorldBankDataRetriever("SP.DYN.LE00.IN", is_rate=True),
            WorldBankDataRetriever("SP.POP.65UP.TO.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("SP.POP.TOTL"),
            WorldBankDataRetriever("VC.IHR.PSRC.P5", min_year_range=[2000, 2002]),
        ],
        "name": "Asia",
        "crs": "+proj=lcc +lat_1=15 +lat_2=45 +lat_0=30 +lon_0=100 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs",
        "legends": {
            "description": [(0.035, 0.022), "left", "bottom"],
            "source": [(0.035, 0.95), "left", "top"],
            "attribution": [(0.965, 0.95), "right", "top"]
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
        "retrievers" : [
            DebtRetrieval("Debt as % of GDP", is_rate=True),
            WorldBankDataRetriever("EG.USE.COMM.FO.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("EG.USE.PCAP.KG.OE"),
            WorldBankDataRetriever("GC.TAX.TOTL.GD.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("MS.MIL.XPND.GD.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("NY.ADJ.NNTY.PC.KD"),
            WorldBankDataRetriever("NY.GDP.PCAP.KN"),
            WorldBankDataRetriever("SH.ALC.PCAP.LI", min_year_range=[2000, 2001]),
            WorldBankDataRetriever("SH.MED.PHYS.ZS"),
            WorldBankDataRetriever("SL.GDP.PCAP.EM.KD"),
            WorldBankDataRetriever("SL.TLF.TOTL.IN"),
            WorldBankDataRetriever("SM.POP.RHCR.EA", is_rate=True),
            WorldBankDataRetriever("SP.DYN.CBRT.IN", is_rate=True),
            WorldBankDataRetriever("SP.DYN.LE00.IN", is_rate=True),
            WorldBankDataRetriever("SP.POP.65UP.TO.ZS", is_rate=True, round=1),
            WorldBankDataRetriever("SP.POP.TOTL"),
            WorldBankDataRetriever("VC.IHR.PSRC.P5", min_year_range=[2000, 2002]),
        ],
        "crs": "3035",
        "legends": {
            "description": [(0.965, 0.95), "right", "top"],
            "source": [(0.035, 0.022), "left", "bottom"],
            "attribution": [(0.965, 0.022), "right", "bottom"]
        },
        "map_limits": {
            "minx": 2620000,
            "maxx": 7600000,
            "miny": 1440000,
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
            # Country.LIECHTENSTEIN,
            Country.LITHUANIA,
            Country.LUXEMBOURG,
            Country.MOLDOVA,
            Country.NORTH_MACEDONIA,
            Country.MALTA,
            # Country.MONACO,
            Country.MONTENEGRO,
            Country.NETHERLANDS,
            Country.NORWAY,
            Country.POLAND,
            Country.PORTUGAL,
            Country.ROMANIA,
            Country.RUSSIA,
            # Country.SAN_MARINO,
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


