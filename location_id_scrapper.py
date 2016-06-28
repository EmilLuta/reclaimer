import requests

from app.models import LocationSeed, DestinationData
from app import db

request_base = 'http://lookup.hotels.com/2/suggest/v1.3/json?' \
               'locale=en_IE&&query='

location_seed_number = LocationSeed.query.count()
index = 0


for location_seed in LocationSeed.query.all():
    r = requests.get(request_base + location_seed.city_name.replace(',', '') + '++' + location_seed.country_name.replace(',', ''))
    try:
        destination_data_dict = r.json()['suggestions'][0]['entities'][0]
        destination_data = DestinationData(
            location_seed_id=location_seed.id,
            longitude=destination_data_dict['longitude'],
            latitude=destination_data_dict['latitude'],
            destination_id=destination_data_dict['destinationId']
        )
    except Exception:
        print("No data available for {} {}".format(location_seed.city_name, location_seed.country_name))
    try:
        db.session.add(destination_data)
        db.session.commit()
    except Exception:
        print("Invalid operations?")
    index += 1
    print("Processing numbers: {}/{}.".format(index, location_seed_number))