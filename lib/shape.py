import geopandas as gpd
from shapely.geometry import Polygon

# This script is used to keep only the European part of Russia from a full country shapefile.

gdf = gpd.read_file("maps/gadm41_RUS_00.json")

# 2) Make sure it's in WGS84 (lon/lat)
if gdf.crs is None or gdf.crs.to_string().lower() not in ("epsg:4326", "wgs84"):
    gdf = gdf.to_crs("EPSG:4326")

# 3) Build a big polygon for the world WEST of 60°E
west_of_60 = Polygon([(-180,-90), (60,-90), (60,90), (-180,90)])

# 4) Intersect Russia with that polygon (keeps only European part)
europe_russia = gdf.copy()
europe_russia["geometry"] = europe_russia.geometry.intersection(west_of_60)

# 5) Drop empty pieces and explode multipart geometries
europe_russia = europe_russia[~europe_russia.is_empty & europe_russia.geometry.notnull()]
europe_russia = europe_russia.explode(ignore_index=True)

# 6) Save result
europe_russia.to_file("gadm41_RUS_0_europe.json", driver="GeoJSON")
print("Saved: gadm41_RUS_0_europe.json")
