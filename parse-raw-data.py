import csv
import argparse
import requests

parser = argparse.ArgumentParser(description='Process raw census data')
parser.add_argument('input', metavar='I', help='input file')
parser.add_argument('google_maps_api_key', help='google maps api key')
parser.add_argument('output', help='output file')

args = parser.parse_args()

GOOGLE_MAP_REQUEST_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='

output_file = open(args.output, "w")
output_file.write('name,pop,lat,lon\n')

with open(args.input) as f:
    lines = f.readlines()
    for line in lines:
        index = 0
        for row in csv.reader(line, delimiter=','):
            if index == 0:
                city_state = row[0]
                city_only = city_state.split(',')[0]
                modified_city = city_state.replace(' ', '+')
                request_string = GOOGLE_MAP_REQUEST_URL + modified_city + '&key=' + args.google_maps_api_key
                r = requests.get(request_string)
                result_json = r.json()
                first_item = result_json['results'][0]
                coordinates = first_item['geometry']['location']
                latitude = coordinates['lat']
                longitude = coordinates['lng']
            if index == 2:
                population = str(row[0]).replace(',', '')
            if index == 3:
                print('processing ' + city_state)
                combined_string = city_only + ',' + str(population) + ',' + str(latitude) + ','\
                                  + str(longitude) + '\n'
                output_file.write(combined_string)
            index += 1

output_file.close()
