import requests
from app.models import LocationSeed
from app import db

from string import ascii_lowercase

request_base = 'http://www.numbeo.com/common/CitySearchJson'

for char1 in ascii_lowercase:
    for char2 in ascii_lowercase:

        r = requests.get(request_base + '?term={}{}'.format(char1, char2))

        for country_data in r.json():
            city_name = str(country_data['label'].split(',')[0])
            country_name = ', '.join([data.strip() for data in country_data['label'].split(',')][1:])
            if not '?' in country_name and not '?' in city_name:
                location_seed = LocationSeed(
                    country_name=country_name,
                    city_name=city_name
                )
                db.session.add(location_seed)
                db.session.commit()
        print("Finishing pair: {}{}".format(char1, char2))
