from enum import Enum


class Country(Enum):
    ALBANIA = {
        "name": "Albania",
        "iso2": "AL",
        "iso3": "ALB",
    }
    ANDORRA = {
        "name": "Andorra",
        "iso2": "AD",
        "iso3": "AND",
    }
    ARMENIA = {
        "name": "Armenia",
        "iso2": "AM",
        "iso3": "ARM",
    }
    AUSTRIA = {
        "name": "Austria",
        "iso2": "AT",
        "iso3": "AUT",
    }
    AZERBAIJAN = {
        "name": "Azerbaijan",
        "iso2": "AZ",
        "iso3": "AZE",
    }
    BELARUS = {
        "name": "Belarus",
        "iso2": "BY",
        "iso3": "BLR",
    }
    BELGIUM = {
        "name": "Belgium",
        "iso2": "BE",
        "iso3": "BEL",
    }
    BOSNIA_HERZEGOVINA = {
        "name": "Bosnia and Herzegovina",
        "iso2": "BA",
        "iso3": "BIH",
    }
    BULGARIA = {
        "name": "Bulgaria",
        "iso2": "BG",
        "iso3": "BGR",
    }
    CROATIA = {
        "name": "Croatia",
        "iso2": "HR",
        "iso3": "HRV",
    }
    CYPRUS = {
        "name": "Cyprus",
        "iso2": "CY",
        "iso3": "CYP",
    }
    CZECHIA = {
        "name": "Czech Republic",
        "iso2": "CZ",
        "iso3": "CZE",
    }
    DENMARK = {
        "name": "Denmark",
        "iso2": "DK",
        "iso3": "DNK",
    }
    ESTONIA = {
        "name": "Estonia",
        "iso2": "EE",
        "iso3": "EST",
    }
    FINLAND = {
        "name": "Finland",
        "iso2": "FI",
        "iso3": "FIN",
    }
    FRANCE = {
        "name": "France",
        "iso2": "FR",
        "iso3": "FRA",
    }
    GEORGIA = {
        "name": "Georgia",
        "iso2": "GE",
        "iso3": "GEO",
    }
    GERMANY = {
        "name": "Germany",
        "iso2": "DE",
        "iso3": "DEU",
    }
    GREECE = {
        "name": "Greece",
        "iso2": "GR",
        "iso3": "GRC",
    }
    HUNGARY = {
        "name": "Hungary",
        "iso2": "HU",
        "iso3": "HUN",
    }
    ICELAND = {
        "name": "Iceland",
        "iso2": "IS",
        "iso3": "ISL",
    }
    IRELAND = {
        "name": "Ireland",
        "iso2": "IE",
        "iso3": "IRL",
    }
    ITALY = {
        "name": "Italy",
        "iso2": "IT",
        "iso3": "ITA",
    }
    LITHUANIA = {
        "name": "Lithuania",
        "iso2": "LT",
        "iso3": "LTU",
    }
    LUXEMBOURG = {
        "name": "Luxembourg",
        "iso2": "LU",
        "iso3": "LUX",
    }
    NORTH_MACEDONIA = {
        "name": "North Macedonia",
        "iso2": "MK",
        "iso3": "MKD",
    }
    MALTA = {
        "name": "Malta",
        "iso2": "MT",
        "iso3": "MLT",
    }
    MOLDOVA = {
        "name": "Moldova",
        "iso2": "MD",
        "iso3": "MDA",
    }
    MONACO = {
        "name": "Monaco",
        "iso2": "MC",
        "iso3": "MCO",
    }
    MONTENEGRO = {
        "name": "Montenegro",
        "iso2": "ME",
        "iso3": "MNE",
    }
    NETHERLANDS = {
        "name": "Netherlands",
        "iso2": "NL",
        "iso3": "NLD",
    }
    NORWAY = {
        "name": "Norway",
        "iso2": "NO",
        "iso3": "NOR",
    }
    POLAND = {
        "name": "Poland",
        "iso2": "PL",
        "iso3": "POL",
    }
    PORTUGAL = {
        "name": "Portugal",
        "iso2": "PT",
        "iso3": "PRT",
    }
    ROMANIA = {
        "name": "Romania",
        "iso2": "RO",
        "iso3": "ROU",
    }
    SERBIA = {
        "name": "Serbia",
        "iso2": "RS",
        "iso3": "SRB",
    }
    SLOVAKIA = {
        "name": "Slovakia",
        "iso2": "SK",
        "iso3": "SVK",
    }
    SLOVENIA = {
        "name": "Slovenia",
        "iso2": "SI",
        "iso3": "SVN",
    }
    SPAIN = {
        "name": "Spain",
        "iso2": "ES",
        "iso3": "ESP",
    }
    SWEDEN = {
        "name": "Sweden",
        "iso2": "SE",
        "iso3": "SWE",
    }
    SWITZERLAND = {
        "name": "Switzerland",
        "iso2": "CH",
        "iso3": "CHE",
    }
    TURKEY = {
        "name": "Turkey",
        "iso2": "TR",
        "iso3": "TUR",
    }
    UKRAINE = {
        "name": "Ukraine",
        "iso2": "UA",
        "iso3": "UKR",
    }
    UNITED_KINGDOM = {
        "name": "United Kingdom",
        "iso2": "GB",
        "iso3": "GBR",
    }
    LIECHTENSTEIN = {
        "name": "Liechtenstein",
        "iso2": "LI",
        "iso3": "LIE",
    }
    SAN_MARINO = {
        "name": "San Marino",
        "iso2": "SM",
        "iso3": "SMR",
    }
    LATVIA = {
        "name": "Latvia",
        "iso2": "LV",
        "iso3": "LVA",
    }
    KOSOVO = {
        "name": "Kosovo",
        "iso2": "XK",
        "iso3": "KOS",
    }
    RUSSIA = {
        "name": "Russian Federation",
        "iso2": "RU",
        "iso3": "RUS",
    }

    @staticmethod
    def get_by_iso2(iso2):
        for country in Country:
            if country.iso2 == iso2:
                return country
        return None

    @staticmethod
    def get_by_iso3(iso3):
        for country in Country:
            if country.iso3 == iso3:
                return country
        return None

    @staticmethod
    def get_by_name(name):
        for country in Country:
            if country.name == name:
                return country
        return None

    @staticmethod
    def all_iso2():
        return [country.iso2 for country in Country]

    @staticmethod
    def all_iso3():
        return [country.iso3 for country in Country]

    @staticmethod
    def all_names():
        return [country.name for country in Country]

    @staticmethod
    def all():
        return [country for country in Country]

    @property
    def name(self):
        return self.value["name"]

    @property
    def iso2(self):
        return self.value["iso2"]

    @property
    def iso3(self):
        return self.value["iso3"]

    @property
    def label_size(self):
        if self in [Country.SLOVENIA]:
            return 11
        if self in [Country.NORTH_MACEDONIA, Country.CROATIA, Country.KOSOVO, Country.ALBANIA, Country.LUXEMBOURG]:
            return 12
        if self in [Country.SERBIA, Country.ESTONIA, Country.NETHERLANDS, Country.BOSNIA_HERZEGOVINA,
                    Country.DENMARK, Country.MONTENEGRO]:
            return 13
        return 15

    @property
    def label_coords(self):
        if self == Country.RUSSIA:
            return 6400000, 4300000
        if self == Country.ALBANIA:
            return 5150000, 2050000
        if self == Country.AUSTRIA:
            return 4670000, 2700000
        if self == Country.SWITZERLAND:
            return 4185571, 2650000
        if self == Country.CYPRUS:
            return 6520000, 1600000
        if self == Country.CZECHIA:
            return 4705309, 2953169
        if self == Country.DENMARK:
            return 4280000, 3649679
        if self == Country.FINLAND:
            return 5100655, 4399000
        if self == Country.UNITED_KINGDOM:
            return 3500000, 3311356
        if self == Country.GREECE:
            return 5300000, 1900000
        if self == Country.CROATIA:
            return 4854665, 2520007
        if self == Country.LATVIA:
            return 5270000, 3845716
        if self == Country.SLOVENIA:
            return 4690000, 2568867
        if self == Country.SWEDEN:
            return 4580000, 4000000
        if self == Country.NORWAY:
            return 4300000, 4200000
        return None, None


exceptions = {
    "Czechia": Country.CZECHIA,
    "Turkiye": Country.TURKEY,
    "Slovak Republic": Country.SLOVAKIA,
    "Russia": Country.RUSSIA,
}


def names_to_iso3(name):
    try:
        return Country.get_by_name(name).iso3
    except:
        if name in exceptions:
            return exceptions[name].iso3
        print(f"Could not find iso3 for {name}")
        return None


def names_to_iso2(name):
    try:
        return Country.get_by_name(name).iso2
    except:
        if name in exceptions:
            return exceptions[name].iso2
        print(f"Could not find iso2 for {name}")
        return None
