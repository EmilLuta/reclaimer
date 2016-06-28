import requests

from app import db
from app.models import IATACode
index = 0

r = requests.get('https://iatacodes.org/api/v6/cities?api_key=c4d8df44-cf29-42eb-abf0-2b8aa440c0c8')
iata_codes = r.json()['response']
number = len(iata_codes)

for iata_code in iata_codes:
    iata = IATACode(code=iata_code['code'], name=iata_code['name'], country_code=iata_code['country_code'])
    db.session.add(iata)
    db.session.commit()
    index += 1
    print("Processing numbers: {}/{}.".format(index, number))