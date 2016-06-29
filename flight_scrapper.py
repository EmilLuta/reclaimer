import re, time

from app.models import LocationSeed, IATACode, Flight
from app import db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

location_seed_number = LocationSeed.query.count()
index = 0

request_base = 'https://www.kayak.com/flights/CLJ-'
driver = webdriver.Chrome('/home/emil/Facultate/An3/Sem2/BusinessIntelligence/reclaimer/chromedriver')


for location_seed in LocationSeed.query.all():
    try:
        driver.get(request_base + IATACode.query.filter(IATACode.name.ilike('%{}%'.format(location_seed.city_name))).first().code + '/' + '2016-08-15/2016-08-22')
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "resultsListHeader"))
            )
        except Exception:
            print("No data available for {} {}".format(
                location_seed.city_name,
                location_seed.country_name)
            )
        finally:
            try:
                alert = driver.switch_to.alert
                alert.dismiss()
            except Exception:
                pass
            try:
                driver.find_element_by_class_name('r9-dialog-closeButton').click()
            except Exception:
                pass
            time.sleep(5)
            try:
                price_string = driver.find_elements_by_class_name('flightresult')[0].find_elements_by_class_name('pricerange')[0].text
                if price_string.replace('$', '').isdigit():
                    price = int(price_string.replace('$', ''))
                else:
                    raise ValueError()
                site = driver.find_elements_by_class_name('bookitprice')[0].get_attribute('href')
                flight = Flight(price=price, site=site, location_seed_id=location_seed.id)
                db.session.add(flight)
                db.session.commit()
            except Exception:
                print('Invalid information on the page')
    except Exception:
        print('Invalid information: {}, {}'.format(location_seed.city_name, location_seed.country_name))

    index += 1
    print("Processing numbers: {}/{}.".format(index, location_seed_number))
driver.quit()
