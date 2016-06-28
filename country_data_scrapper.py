import bs4
import requests
from app.models import LocationSeed, LocationData
from app import db

request_base = 'http://www.numbeo.com/cost-of-living/city_result.jsp'

location_seed_number = LocationSeed.query.count()
index = 0

for location_seed in LocationSeed.query.all():
    r = requests.get(request_base + '?country=' + location_seed.country_name + '&city=' + location_seed.city_name)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    try:
        location_data_dict = {}
        location_data_dict['restaurant_inexpensive_meal'] = soup.find(
            text="Meal, Inexpensive Restaurant ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        location_data_dict['restaurant_decent_couple_meal'] = soup.find(
            text="Meal for 2 People, Mid-range Restaurant, Three-course ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')

        if soup.find(text="Domestic Beer (0.5 liter draught) ") is not None:
            location_data_dict['local_beverage'] = soup.find(
                text="Domestic Beer (0.5 liter draught) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        elif soup.find(text="Domestic Non-Alcoholic Beer (0.5 liter draught) ") is not None:
            location_data_dict['local_beverage'] = soup.find(
                text="Domestic Non-Alcoholic Beer (0.5 liter draught) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        else:
            print("{}: NO LOCAL BEVERAGE WAS FOUND!".format(location_seed.city_name))

        if soup.find(text="Imported Beer (0.33 liter bottle) ") is not None:
            location_data_dict['imported_beverage'] = soup.find(
                text="Imported Beer (0.33 liter bottle) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        elif soup.find(text="Imported Non-Alcoholic Beer (0.33 liter bottle) ") is not None:
            location_data_dict['imported_beverage'] = soup.find(
                text="Imported Non-Alcoholic Beer (0.33 liter bottle) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        else:
            print("{}: NO IMPORTED BEVERAGE WAS FOUND!".format(location_seed.city_name))

        location_data_dict['coffee'] = soup.find(
            text="Cappuccino (regular) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        location_data_dict['soda'] = soup.find(
            text="Coke/Pepsi (0.33 liter bottle) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        location_data_dict['water'] = soup.find(
            text="Water (0.33 liter bottle)  ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        location_data_dict['ticket_transport'] = soup.find(
            text="One-way Ticket (Local Transport) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        location_data_dict['taxi_start'] = soup.find(
            text="Taxi Start (Normal Tariff) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        location_data_dict['taxi_km'] = soup.find(
            text="Taxi 1km (Normal Tariff) ").find_parent().next_sibling.next_sibling.text.strip().replace('\xa0', '')
        location_data = LocationData(
            location_seed_id=location_seed.id,
            restaurant_inexpensive_meal=location_data_dict['restaurant_inexpensive_meal'],
            restaurant_decent_couple_meal=location_data_dict['restaurant_decent_couple_meal'],
            local_beverage=location_data_dict['local_beverage'],
            imported_beverage=location_data_dict['imported_beverage'],
            coffee=location_data_dict['coffee'],
            soda=location_data_dict['soda'],
            water=location_data_dict['water'],
            ticket_transport=location_data_dict['ticket_transport'],
            taxi_start=location_data_dict['taxi_start'],
            taxi_km=location_data_dict['taxi_km']
        )
        db.session.add(location_data)
        db.session.commit()
    except Exception:
        print("FOUND EXCEPTION - {} {}".format(location_seed.country_name, location_seed.city_name))

    index += 1

    print("Processing numbers: {}/{}.".format(index, location_seed_number))
