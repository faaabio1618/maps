from enum import Enum
from functools import lru_cache


class Country(Enum):
    ALBANIA = {
        "name": "Albania",
        "iso2": "AL",
        "iso3": "ALB",
    }

    ANDORRA = {
        "show_value": False,
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
    EGYPT = {
        "name": "Egypt",
        "iso2": "EG",
        "iso3": "EGY",
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
    KAZAKHSTAN = {
        "name": "Kazakhstan",
        "iso2": "KZ",
        "iso3": "KAZ",
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
        "show_value": False,
        "iso2": "LI",
        "iso3": "LIE",
    }
    SAN_MARINO = {
        "show_value": False,
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

    CHINA = {
        "name": "China",
        "iso2": "CN",
        "iso3": "CHN",
    }
    JAPAN = {
        "name": "Japan",
        "iso2": "JP",
        "iso3": "JPN",
    }

    # Asia countries
    AFGHANISTAN = {
        "name": "Afghanistan",
        "iso2": "AF",
        "iso3": "AFG",
    }
    BAHRAIN = {
        "name": "Bahrain",
        "iso2": "BH",
        "iso3": "BHR",
    }
    TAIWAN = {
        "name": "Taiwan",
        "iso2": "TW",
        "iso3": "TWN",
    }
    BANGLADESH = {
        "name": "Bangladesh",
        "iso2": "BD",
        "iso3": "BGD",
    }
    BHUTAN = {
        "name": "Bhutan",
        "iso2": "BT",
        "iso3": "BTN",
    }
    BRUNEI = {
        "name": "Brunei",
        "iso2": "BN",
        "iso3": "BRN",
    }
    CAMBODIA = {
        "name": "Cambodia",
        "iso2": "KH",
        "iso3": "KHM",
    }
    EAST_TIMOR = {
        "name": "East Timor",
        "iso2": "TL",
        "iso3": "TLS",
    }
    INDIA = {
        "name": "India",
        "iso2": "IN",
        "iso3": "IND",
    }
    INDONESIA = {
        "name": "Indonesia",
        "iso2": "ID",
        "iso3": "IDN",
    }
    IRAN = {
        "name": "Iran",
        "iso2": "IR",
        "iso3": "IRN",
    }
    IRAQ = {
        "name": "Iraq",
        "iso2": "IQ",
        "iso3": "IRQ",
    }
    ISRAEL = {
        "name": "Israel",
        "iso2": "IL",
        "iso3": "ISR",
    }
    JORDAN = {
        "name": "Jordan",
        "iso2": "JO",
        "iso3": "JOR",
    }
    KUWAIT = {
        "name": "Kuwait",
        "iso2": "KW",
        "iso3": "KWT",
    }
    KYRGYZSTAN = {
        "name": "Kyrgyzstan",
        "iso2": "KG",
        "iso3": "KGZ",
    }
    LAOS = {
        "name": "Laos",
        "iso2": "LA",
        "iso3": "LAO",
    }
    LEBANON = {
        "name": "Lebanon",
        "iso2": "LB",
        "iso3": "LBN",
    }
    MALAYSIA = {
        "name": "Malaysia",
        "iso2": "MY",
        "iso3": "MYS",
    }
    MALDIVES = {
        "name": "Maldives",
        "iso2": "MV",
        "iso3": "MDV",
    }
    MONGOLIA = {
        "name": "Mongolia",
        "iso2": "MN",
        "iso3": "MNG",
    }
    MYANMAR = {
        "name": "Myanmar",
        "iso2": "MM",
        "iso3": "MMR",
    }
    NEPAL = {
        "name": "Nepal",
        "iso2": "NP",
        "iso3": "NPL",
    }
    NORTH_KOREA = {
        "name": "North Korea",
        "iso2": "KP",
        "iso3": "PRK",
    }
    OMAN = {
        "name": "Oman",
        "iso2": "OM",
        "iso3": "OMN",
    }
    PAKISTAN = {
        "name": "Pakistan",
        "iso2": "PK",
        "iso3": "PAK",
    }
    PALESTINE = {
        "name": "Palestine",
        "iso2": "PS",
        "iso3": "PSX",
    }
    PHILIPPINES = {
        "name": "Philippines",
        "iso2": "PH",
        "iso3": "PHL",
    }
    QATAR = {
        "name": "Qatar",
        "iso2": "QA",
        "iso3": "QAT",
    }
    SAUDI_ARABIA = {
        "name": "Saudi Arabia",
        "iso2": "SA",
        "iso3": "SAU",
    }
    SINGAPORE = {
        "name": "Singapore",
        "iso2": "SG",
        "iso3": "SGP",
    }
    SOUTH_KOREA = {
        "name": "South Korea",
        "iso2": "KR",
        "iso3": "KOR",
    }
    SRI_LANKA = {
        "name": "Sri Lanka",
        "iso2": "LK",
        "iso3": "LKA",
    }
    SYRIA = {
        "name": "Syria",
        "iso2": "SY",
        "iso3": "SYR",
    }
    TAJIKISTAN = {
        "name": "Tajikistan",
        "iso2": "TJ",
        "iso3": "TJK",
    }
    THAILAND = {
        "name": "Thailand",
        "iso2": "TH",
        "iso3": "THA",
    }
    TURKMENISTAN = {
        "name": "Turkmenistan",
        "iso2": "TM",
        "iso3": "TKM",
    }
    UNITED_ARAB_EMIRATES = {
        "name": "United Arab Emirates",
        "iso2": "AE",
        "iso3": "ARE",
    }
    UZBEKISTAN = {
        "name": "Uzbekistan",
        "iso2": "UZ",
        "iso3": "UZB",
    }
    HOLY_SEE = {
        "show_value": False,
        "name": "Holy See",
        "iso2": "VA",
        "iso3": "VAT",
    }
    VIETNAM = {
        "name": "Vietnam",
        "iso2": "VN",
        "iso3": "VNM",
    }
    YEMEN = {
        "name": "Yemen",
        "iso2": "YE",
        "iso3": "YEM",
    }

    UNITED_STATES = {
        "name": "United States",
        "iso2": "US",
        "iso3": "USA",
    }
    CANADA = {
        "name": "Canada",
        "iso2": "CA",
        "iso3": "CAN",
    }
    MEXICO = {
        "name": "Mexico",
        "iso2": "MX",
        "iso3": "MEX",
    }
    FRENCH_GUYANA = {
        "name": "French Guiana",
        "iso2": "GF",
        "iso3": "GUF",
        "territory": True
    }
    BRAZIL = {
        "name": "Brazil",
        "iso2": "BR",
        "iso3": "BRA",
    }
    ARGENTINA = {
        "name": "Argentina",
        "iso2": "AR",
        "iso3": "ARG",
    }
    COLOMBIA = {
        "name": "Colombia",
        "iso2": "CO",
        "iso3": "COL",
    }
    VENEZUELA = {
        "name": "Venezuela",
        "iso2": "VE",
        "iso3": "VEN",
    }
    PERU = {
        "name": "Peru",
        "iso2": "PE",
        "iso3": "PER",
    }
    CHILE = {
        "name": "Chile",
        "iso2": "CL",
        "iso3": "CHL",
    }
    BOLIVIA = {
        "name": "Bolivia",
        "iso2": "BO",
        "iso3": "BOL",
    }
    PARAGUAY = {
        "name": "Paraguay",
        "iso2": "PY",
        "iso3": "PRY",
    }
    URUGUAY = {
        "name": "Uruguay",
        "iso2": "UY",
        "iso3": "URY",
    }
    GUYANA = {
        "name": "Guyana",
        "iso2": "GY",
        "iso3": "GUY",
    }
    SURINAME = {
        "name": "Suriname",
        "iso2": "SR",
        "iso3": "SUR",
    }
    ECUADOR = {
        "name": "Ecuador",
        "iso2": "EC",
        "iso3": "ECU",
    }
    PANAMA = {
        "name": "Panama",
        "iso2": "PA",
        "iso3": "PAN",
    }
    COSTA_RICA = {
        "name": "Costa Rica",
        "iso2": "CR",
        "iso3": "CRI",
    }
    NICARAGUA = {
        "name": "Nicaragua",
        "iso2": "NI",
        "iso3": "NIC",
    }
    HONDURAS = {
        "name": "Honduras",
        "iso2": "HN",
        "iso3": "HND",
    }
    EL_SALVADOR = {
        "name": "El Salvador",
        "iso2": "SV",
        "iso3": "SLV",
    }
    GUATEMALA = {
        "name": "Guatemala",
        "iso2": "GT",
        "iso3": "GTM",
    }
    BELIZE = {
        "name": "Belize",
        "iso2": "BZ",
        "iso3": "BLZ",
    }
    CUBA = {
        "name": "Cuba",
        "iso2": "CU",
        "iso3": "CUB",
    }
    DOMINICAN_REPUBLIC = {
        "name": "Dominican Republic",
        "iso2": "DO",
        "iso3": "DOM",
    }
    HAITI = {
        "name": "Haiti",
        "iso2": "HT",
        "iso3": "HTI",
    }
    JAMAICA = {
        "name": "Jamaica",
        "iso2": "JM",
        "iso3": "JAM",
    }
    TRINIDAD_TOBAGO = {
        "name": "Trinidad and Tobago",
        "iso2": "TT",
        "iso3": "TTO",
    }
    BAHAMAS = {
        "name": "Bahamas",
        "iso2": "BS",
        "iso3": "BHS",
    }
    PUERTO_RICO = {
        "name": "Puerto Rico",
        "iso2": "PR",
        "iso3": "PRI",
    }
    BARBADOS = {
        "name": "Barbados",
        "iso2": "BB",
        "iso3": "BRB",
    }
    ANTIGUA_BARBUDA = {
        "name": "Antigua and Barbuda",
        "iso2": "AG",
        "iso3": "ATG",
    }
    SAINT_LUCIA = {
        "name": "Saint Lucia",
        "iso2": "LC",
        "iso3": "LCA",
    }

    AUSTRALIA = {
        "name": "Australia",
        "iso2": "AU",
        "iso3": "AUS",
    }
    NEW_ZEALAND = {
        "name": "New Zealand",
        "iso2": "NZ",
        "iso3": "NZL",
    }
    FIJI = {
        "name": "Fiji",
        "iso2": "FJ",
        "iso3": "FJI",
    }
    PAPUA_NEW_GUINEA = {
        "name": "Papua New Guinea",
        "iso2": "PG",
        "iso3": "PNG",
    }
    SOLOMON_ISLANDS = {
        "name": "Solomon Islands",
        "iso2": "SB",
        "iso3": "SLB",
    }
    VANUATU = {
        "name": "Vanuatu",
        "iso2": "VU",
        "iso3": "VUT",
    }
    SAMOA = {
        "name": "Samoa",
        "iso2": "WS",
        "iso3": "WSM",
    }
    TONGA = {
        "name": "Tonga",
        "iso2": "TO",
        "iso3": "TON",
    }
    MICRONESIA = {
        "name": "Micronesia (Federated States of)",
        "iso2": "FM",
        "iso3": "FSM",
    }
    KIRIBATI = {
        "name": "Kiribati",
        "iso2": "KI",
        "iso3": "KIR",
    }
    NEW_CALEDONIA = {
        "name": "New Caledonia",
        "iso2": "NC",
        "iso3": "NCL",
        "territory": True
    }
    FRENCH_POLYNESIA = {
        "name": "French Polynesia",
        "iso2": "PF",
        "iso3": "PYF",
        "territory": True
    }
    GUAM = {
        "name": "Guam",
        "iso2": "GU",
        "iso3": "GUM",
        "territory": True
    }
    NAURU = {
        "name": "Nauru",
        "iso2": "NR",
        "iso3": "NRU",
    }
    PALAU = {
        "name": "Palau",
        "iso2": "PW",
        "iso3": "PLW",
    }
    MARSHALL_ISLANDS = {
        "name": "Marshall Islands",
        "iso2": "MH",
        "iso3": "MHL",
    }
    TUVALU = {
        "name": "Tuvalu",
        "iso2": "TV",
        "iso3": "TUV",
    }
    AMERICAN_SAMOA = {
        "name": "American Samoa",
        "iso2": "AS",
        "iso3": "ASM",
        "territory": True
    }
    NORTHERN_MARIANA_ISLANDS = {
        "name": "Northern Mariana Islands",
        "iso2": "MP",
        "iso3": "MNP",
        "territory": True
    }

    ALGERIA = {
        "name": "Algeria",
        "iso2": "DZ",
        "iso3": "DZA",
    }
    ANGOLA = {
        "name": "Angola",
        "iso2": "AO",
        "iso3": "AGO",
    }
    BENIN = {
        "name": "Benin",
        "iso2": "BJ",
        "iso3": "BEN",
    }
    BOTSWANA = {
        "name": "Botswana",
        "iso2": "BW",
        "iso3": "BWA",
    }
    BURKINA_FASO = {
        "name": "Burkina Faso",
        "iso2": "BF",
        "iso3": "BFA",
    }
    BURUNDI = {
        "name": "Burundi",
        "iso2": "BI",
        "iso3": "BDI",
    }
    CABO_VERDE = {
        "name": "Cabo Verde",
        "iso2": "CV",
        "iso3": "CPV",
    }
    CAMEROON = {
        "name": "Cameroon",
        "iso2": "CM",
        "iso3": "CMR",
    }
    CENTRAL_AFRICAN_REPUBLIC = {
        "name": "Central African Republic",
        "iso2": "CF",
        "iso3": "CAF",
    }
    CHAD = {
        "name": "Chad",
        "iso2": "TD",
        "iso3": "TCD",
    }
    COMOROS = {
        "name": "Comoros",
        "iso2": "KM",
        "iso3": "COM",
    }
    CONGO = {
        "name": "Congo",
        "iso2": "CG",
        "iso3": "COG",
    }
    DEMOCRATIC_REPUBLIC_OF_THE_CONGO = {
        "name": "Democratic Republic of the Congo",
        "iso2": "CD",
        "iso3": "COD",
    }
    DJIBOUTI = {
        "name": "Djibouti",
        "iso2": "DJ",
        "iso3": "DJI",
    }
    EQUATORIAL_GUINEA = {
        "name": "Equatorial Guinea",
        "iso2": "GQ",
        "iso3": "GNQ",
    }
    ERITREA = {
        "name": "Eritrea",
        "iso2": "ER",
        "iso3": "ERI",
    }
    ESWATINI = {
        "name": "Eswatini",
        "iso2": "SZ",
        "iso3": "SWZ",
    }
    ETHIOPIA = {
        "name": "Ethiopia",
        "iso2": "ET",
        "iso3": "ETH",
    }
    GABON = {
        "name": "Gabon",
        "iso2": "GA",
        "iso3": "GAB",
    }
    GAMBIA = {
        "name": "Gambia",
        "iso2": "GM",
        "iso3": "GMB",
    }
    GHANA = {
        "name": "Ghana",
        "iso2": "GH",
        "iso3": "GHA",
    }
    GUINEA = {
        "name": "Guinea",
        "iso2": "GN",
        "iso3": "GIN",
    }
    GUINEA_BISSAU = {
        "name": "Guinea-Bissau",
        "iso2": "GW",
        "iso3": "GNB",
    }
    COTE_DIVOIRE = {
        "name": "Cote d'Ivoire",
        "iso2": "CI",
        "iso3": "CIV",
    }
    KENYA = {
        "name": "Kenya",
        "iso2": "KE",
        "iso3": "KEN",
    }
    LESOTHO = {
        "name": "Lesotho",
        "iso2": "LS",
        "iso3": "LSO",
    }
    LIBERIA = {
        "name": "Liberia",
        "iso2": "LR",
        "iso3": "LBR",
    }
    LIBYA = {
        "name": "Libya",
        "iso2": "LY",
        "iso3": "LBY",
    }
    MADAGASCAR = {
        "name": "Madagascar",
        "iso2": "MG",
        "iso3": "MDG",
    }
    MALAWI = {
        "name": "Malawi",
        "iso2": "MW",
        "iso3": "MWI",
    }
    MALI = {
        "name": "Mali",
        "iso2": "ML",
        "iso3": "MLI",
    }
    MAURITANIA = {
        "name": "Mauritania",
        "iso2": "MR",
        "iso3": "MRT",
    }
    MAURITIUS = {
        "name": "Mauritius",
        "iso2": "MU",
        "iso3": "MUS",
    }
    MOROCCO = {
        "name": "Morocco",
        "iso2": "MA",
        "iso3": "MAR",
    }
    MOZAMBIQUE = {
        "name": "Mozambique",
        "iso2": "MZ",
        "iso3": "MOZ",
    }
    NAMIBIA = {
        "name": "Namibia",
        "iso2": "NA",
        "iso3": "NAM",
    }
    NIGER = {
        "name": "Niger",
        "iso2": "NE",
        "iso3": "NER",
    }
    NIGERIA = {
        "name": "Nigeria",
        "iso2": "NG",
        "iso3": "NGA",
    }
    RWANDA = {
        "name": "Rwanda",
        "iso2": "RW",
        "iso3": "RWA",
    }
    SAO_TOME_PRINCIPE = {
        "name": "Sao Tome and Principe",
        "iso2": "ST",
        "iso3": "STP",
    }
    SENEGAL = {
        "name": "Senegal",
        "iso2": "SN",
        "iso3": "SEN",
    }
    SEYCHELLES = {
        "name": "Seychelles",
        "iso2": "SC",
        "iso3": "SYC",
    }
    SIERRA_LEONE = {
        "name": "Sierra Leone",
        "iso2": "SL",
        "iso3": "SLE",
    }
    SOMALIA = {
        "name": "Somalia",
        "iso2": "SO",
        "iso3": "SOM",
    }
    SOUTH_AFRICA = {
        "name": "South Africa",
        "iso2": "ZA",
        "iso3": "ZAF",
    }
    SOUTH_SUDAN = {
        "name": "South Sudan",
        "iso2": "SS",
        "iso3": "SSD",
    }
    SUDAN = {
        "name": "Sudan",
        "iso2": "SD",
        "iso3": "SDN",
    }
    TANZANIA = {
        "name": "Tanzania",
        "iso2": "TZ",
        "iso3": "TZA",
    }
    TOGO = {
        "name": "Togo",
        "iso2": "TG",
        "iso3": "TGO",
    }
    TUNISIA = {
        "name": "Tunisia",
        "iso2": "TN",
        "iso3": "TUN",
    }
    UGANDA = {
        "name": "Uganda",
        "iso2": "UG",
        "iso3": "UGA",
    }
    WESTERN_SAHARA = {
        "name": "Western Sahara",
        "iso2": "EH",
        "iso3": "ESH",
        "territory": True
    }
    ZAMBIA = {
        "name": "Zambia",
        "iso2": "ZM",
        "iso3": "ZMB",
    }
    ZIMBABWE = {
        "name": "Zimbabwe",
        "iso2": "ZW",
        "iso3": "ZWE",
    }
    REUNION = {
        "name": "Reunion",
        "iso2": "RE",
        "iso3": "REU",
        "territory": True
    }
    MAYOTTE = {
        "name": "Mayotte",
        "iso2": "YT",
        "iso3": "MYT",
        "territory": True
    }
    SAINT_HELENA_ASCENSION_TRISTAN_DA_CUNHA = {
        "name": "Saint Helena, Ascension and Tristan da Cunha",
        "iso2": "SH",
        "iso3": "SHN",
        "territory": True
    }

    @staticmethod
    @lru_cache(maxsize=None)
    def get_by_iso2(iso2):
        for country in Country:
            if country.iso2 == iso2:
                return country
        return None

    @staticmethod
    @lru_cache(maxsize=None)
    def get_by_iso3(iso3):
        for country in Country:
            if country.iso3 == iso3:
                return country
        return None

    @staticmethod
    @lru_cache(maxsize=None)
    def get_by_name(name):
        for country in Country:
            if country.name == name:
                return country
        return None

    @property
    def name(self):
        return self.value["name"]

    @property
    def is_territory(self):
        return self.value.get("territory", False)

    @staticmethod
    def all():
        return [country for country in Country]

    @property
    def iso2(self):
        return self.value["iso2"]

    @property
    def iso3(self):
        return self.value["iso3"]

    @property
    def show_value(self):
        return self.value.get("show_value", True)

    @property
    def label_size(self):
        if self in [Country.SLOVENIA, Country.JORDAN, Country.LEBANON, Country.ISRAEL, Country.PALESTINE]:
            return 11
        if self in [Country.NORTH_MACEDONIA, Country.CROATIA, Country.KOSOVO, Country.ALBANIA, Country.LUXEMBOURG,
                    Country.SYRIA]:
            return 12
        if self in [Country.SERBIA, Country.ESTONIA, Country.NETHERLANDS, Country.BOSNIA_HERZEGOVINA,
                    Country.DENMARK, Country.MONTENEGRO]:
            return 13
        return 15

    @lru_cache(maxsize=None)
    def label_coords(self, region=None):
        from lib.Map import Map
        if self == Country.RUSSIA:
            if region == Map.EUROPE:
                return 6400000, 4300000
            if region == Map.ASIA:
                return 100067, 3000000
            else:
                return 6400000, 4300000
        if self == Country.ALBANIA:
            return 5150000, 2050000
        if self == Country.ANDORRA:
            return 3752269, 2181585
        if self == Country.LIECHTENSTEIN:
            return 4380000, 2650000
        if self == Country.MONACO:
            return 4111356, 2333007
        if self == Country.MALTA:
            return 4890000, 1450000
        if self == Country.SAN_MARINO:
            return 4500000, 2350000
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
        if self == Country.AZERBAIJAN:
            if region == Map.ASIA:
                return -4000000, 2004236
            return None, None
        if self == Country.KAZAKHSTAN:
            if region == Map.EUROPE:
                return 7359144, 3800000
            if region == Map.ASIA:
                return None, None
            return 7359144, 3800000
        if self == Country.BAHRAIN:
            return -4550000, 760000
        if self == Country.SINGAPORE:
            return 700000, -3237000
        if self == Country.ISRAEL:
            return -5750000, 1750000
        if self == Country.PALESTINE:
            return -5500000, 1821409
        if self == Country.MALDIVES:
            return -3000000, -2200000
        if self == Country.OMAN:
            return -4550000, -280000
        if self == Country.IRAQ:
            return -4900000, 1558550
        if self == Country.LEBANON:
            return -5536130, 2100000
        if self == Country.SYRIA:
            return -5200000, 1950000
        if self == Country.JORDAN:
            return -5600000, 1650000
        if self == Country.TAJIKISTAN:
            return -2500000, 1200000
        if self == Country.NEPAL:
            return -1600000, -50000
        if self == Country.JAPAN:
            return 3300000, 1200000
        if self == Country.LAOS:
            return 300000, -1100053
        if self == Country.VIETNAM:
            return 1180000, -1900000
        if self == Country.THAILAND:
            return 107475, -1500000
        if self == Country.MALAYSIA:
            return 300702, -2836987
        if self == Country.INDONESIA:
            if region == Map.ASIA:
                return 1505332, -3398180
            if region == Map.OCEANIA:
                return -2408426, -530239
        if self == Country.EAST_TIMOR:
            return 3702693, -4091964
        if self == Country.BELIZE:
            return -2900000, 954384
        if self == Country.GUATEMALA:
            return -3214000, 751500
        if self == Country.EL_SALVADOR:
            return -3086603, 500000
        if self == Country.HAITI:
            return -1337002, 819074
        if self == Country.SEYCHELLES:
            return  3290468, -1452692

        return None, None


exceptions = {
    "Czechia": Country.CZECHIA,
    "Turkiye": Country.TURKEY,
    "Slovak Republic": Country.SLOVAKIA,
    "Russia": Country.RUSSIA,
    "Brunei Darussalam": Country.BRUNEI,
    "Iran, Islamic Rep.": Country.IRAN,
    "Kyrgyz Republic": Country.KYRGYZSTAN,
    "Korea, Rep.": Country.SOUTH_KOREA,
    "Lao PDR": Country.LAOS,
    "West Bank and Gaza": Country.PALESTINE,
    "Timor-Leste": Country.EAST_TIMOR,
    "Viet Nam": Country.VIETNAM,
    "Yemen, Rep.": Country.YEMEN,
    "Yemen Arab Republic": Country.YEMEN,
    "UAE": Country.UNITED_ARAB_EMIRATES,
    "Bosnia-Herzegovina": Country.BOSNIA_HERZEGOVINA,
    "Syrian Arab Republic": Country.SYRIA,
    "Korea, Dem. People's Rep.": Country.NORTH_KOREA,
    "Korea, Republic of": Country.SOUTH_KOREA,
    "Taiwan Province of China": Country.TAIWAN,
    "Türkiye, Republic of": Country.TURKEY,
    "North Macedonia ": Country.NORTH_MACEDONIA,
    "Egypt, Arab Rep.": Country.EGYPT,
    "Venezuela, RB": Country.VENEZUELA,
    "St. Lucia": Country.SAINT_LUCIA,
    "Puerto Rico (US)": Country.PUERTO_RICO,
    "Bahamas, The": Country.BAHAMAS,
    "Micronesia, Fed. Sts.": Country.MICRONESIA,
    "Congo, Rep.": Country.CONGO,
    "Congo, Republic of" : Country.CONGO,
    "Côte d'Ivoire" : Country.COTE_DIVOIRE,
    "South Sudan, Republic of " : Country.SOUTH_SUDAN,
    "São Tomé and Príncipe" : Country.SAO_TOME_PRINCIPE,
    "Lao P.D.R." : Country.LAOS,


    "Congo, Dem. Rep.": Country.DEMOCRATIC_REPUBLIC_OF_THE_CONGO,
    "Gambia, The": Country.GAMBIA,
    "Somalia, Fed. Rep.": Country.SOMALIA

}


@lru_cache(maxsize=None)
def names_to_iso3(name):
    try:
        return Country.get_by_name(name).iso3
    except:
        if name in exceptions:
            return exceptions[name].iso3
        print(f"Could not find iso3 for {name}")
        return None


@lru_cache(maxsize=None)
def names_to_iso2(name):
    try:
        return Country.get_by_name(name).iso2
    except:
        if name in exceptions:
            return exceptions[name].iso2
        print(f"Could not find iso2 for {name}")
        return None
