import re

from app import db
from app.models import Flight, HotDeal

number = Flight.query.count()
index = 0

for flight in Flight.query.all():
    try:
        location_seed = flight.location_seed
        location_data_id = location_seed.location_data[0].id
        min = int(re.findall(r'\b\d+\b', location_seed.destinations[0].hotels[0].price)[0])
        hotel_id = location_seed.destinations[0].hotels[0].id
        for hotel in location_seed.destinations[0].hotels:
            hotel_price = int(re.findall(r'\b\d+\b', hotel.price)[0])
            if hotel_price < min:
                min = hotel_price
                hotel_id = hotel.id
        hot_deal = HotDeal(flight_id=flight.id, hotel_id=hotel_id, location_data_id=location_data_id, ranking=int(2 * min + flight.price))
        db.session.add(hot_deal)
        db.session.commit()

    except Exception:
        print("Something went wrong.")
    index += 1
    print("Processing numbers: {}/{}.".format(index, number))