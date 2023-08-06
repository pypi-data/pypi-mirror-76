import os

import dotenv

import epiw
from epiw.grid import grid

dotenv.load_dotenv()

api_key = os.environ['API_KEY']

desc = epiw.hourly_weather_desc()

print(desc)

desc = epiw.daily_weather_desc()

print(desc)

values = epiw.hourly_weather('20200101', '20200101', api_key=api_key)

print(values)

values = epiw.read('weather', 'daily', '20180101', '20200101', lonlat='127,37', api_key=api_key)

print(values)

values = epiw.read_as_gpd('weather', 'daily', '20180101', '20200101', lonlat='127,37', api_key=api_key)
print(values)

kma_data = epiw.read_as_gpd('weather', 'daily', '20200101', '20200101', api_key=api_key)
kma_data = kma_data.set_crs(4326).to_crs(5179)
kma_data.drop(['tm'], axis=1).to_file('./tmp/output.json', driver='GeoJSON')
grid('./tmp/output.json', './tmp/output.tiff', 'tn', cell_size=10000)
