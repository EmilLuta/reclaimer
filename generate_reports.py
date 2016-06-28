import pyexcel
import pyexcel_xls
import pyexcel_xlsx
import re

from app.models import Hotel, LocationSeed

output_sheet_1 = {} # Price value
output_sheet_2 = {} # Average per location
output_sheet_3 = {} # Density of locations
regex = '\d+'

# Sheet 1
for hotel in Hotel.query.all():
    try:
        output_sheet_1[int(re.findall(regex, Hotel.query.first().price)[0]) /
                       (float(hotel.trip_advisor_review) * float(hotel.review))] = [hotel.country, hotel.city]
    except:
        output_sheet_1['No Value'] = ['Unknown', 'Unknown']
# Sheet 2
for location_seed in LocationSeed.query.all():
    total_per_destination = 0
    number = 0
    try:
        for hotel in location_seed.location:
            total_per_destination += int(re.findall(regex, hotel.destination.price)[0])
            number += 1
        output_sheet_2[location_seed.country_name] = total_per_destination / number
    except:
        output_sheet_2['Unknown'] = 'No Value'
# Sheet 3
for location_seed in LocationSeed.query.all():
    if location_seed.country_name in output_sheet_3:
        output_sheet_3[location_seed.country_name] += 1
    else:
        output_sheet_3[location_seed.country_name] = 1

content = {
    'Country Popularity': [['Travel Popularity Index', 'Country']],
    'Average': [['Average', 'Country']],
    'Price Value': [['Price Value Index', 'Country', 'City']]
}

for price in reversed(sorted(output_sheet_1.keys())):
    content['Price Value'].append([price, output_sheet_1[price][0], output_sheet_1[price][1]])

for country in reversed(sorted(output_sheet_2.keys())):
    content['Average'].append([output_sheet_2[country], country])

for country in reversed(sorted(output_sheet_3.keys())):
    content['Country Popularity'].append([output_sheet_3[country], country])

book = pyexcel.get_book(bookdict=content)
book.save_as('data_report.xls')
