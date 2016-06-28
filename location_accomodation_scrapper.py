import re

from app.models import DestinationData, Hotel
from app import db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

destination_data_number = DestinationData.query.count()
index = 0

request_base = "http://www.hotels.com/search.do?resolved-location=CITY%3A#{destination_id}%3AUNKNOWN%3AUNKNOWN&" \
               "destination-id=#{destination_id}&q-destination=#{city},%20#{country}&" \
               "q-check-in=#{check_in}&q-check-out=#{check_out}&" \
               "q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=PRICE"

driver = webdriver.Chrome('/home/emil/Facultate/An3/Sem2/BusinessIntelligence/reclaimer/chromedriver')

destination_index = 0
destination_data_number = DestinationData.query.count()

for destination_data in DestinationData.query.all():
    location_seed = destination_data.location_seed
    country = location_seed.country_name
    city = location_seed.city_name
    check_in = '2016-08-15'
    check_out = '2016-08-22'
    computed_url = request_base.replace(
        '#{destination_id}', str(destination_data.destination_id)
    ).replace(
        '#{city}', city
    ).replace(
        '#{country}', country
    ).replace(
        '#{check_in}', check_in
    ).replace('#{check_out}', check_out)
    driver.get(computed_url)
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hotel-wrap"))
        )
    except Exception:
        print("No data available for {} {}".format(
            destination_data.location_seed.city_name,
            destination_data.location_seed.country_name)
        )
    finally:
        hotels_data = driver.find_elements_by_class_name('hotel-wrap')
        for hotel_data in hotels_data:
            try:
                regex = '\d*\.\d+|\d+'
                site_url = hotel_data.find_element_by_xpath('//h3[@class="p-name"]/a').get_attribute('href')
                name = hotel_data.find_element_by_xpath('//h3[@class="p-name"]').text
                try:
                    price = hotel_data.find_element_by_xpath('//span[@class="old-price-cont"]')\
                        .find_element_by_tag_name('ins').text
                except:
                    price = hotel_data.find_element_by_xpath('//div[@class="price"]')\
                        .find_element_by_tag_name('b').text
                address = hotel_data.find_element_by_xpath('//p[@class="p-adr"]').text
                review = hotel_data.find_element_by_xpath(
                    '//span[@class="star-rating widget-tooltip widget-tooltip-tr widget-star-rating-overlay"]'
                ).get_attribute('data-star-rating')
                trip_advisor_review = re.findall(
                    regex, hotel_data.find_element_by_xpath('//div[@class="logo-wrap"]'
                                                            ).text)[0]
                h = Hotel.query.filter(Hotel.name == name, Hotel.price == price, Hotel.address == Hotel.address).first()
                h = Hotel.query.filter(Hotel.name == name, Hotel.price == price, Hotel.address == Hotel.address).first()
                if not h:
                    hotel = Hotel(
                        site_url=site_url,
                        name=name,
                        price=price,
                        address=address,
                        review=review,
                        trip_advisor_review=trip_advisor_review,
                        destination_data_id=destination_data.id
                    )
                    db.session.add(hotel)
                    db.session.commit()
            except Exception:
                print("Invalid data?")
    destination_index += 1
    print("Processing numbers: {}/{}.".format(destination_index, destination_data_number))
driver.quit()
