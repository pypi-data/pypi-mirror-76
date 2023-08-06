import requests
import csv





starttime = input('Enter the start time: ')
endtime = input('Enter the end time: ')
latitude = input('Enter the latitude: ')
longitude = input('Enter the longitude: ')
maxradius = input('Enter max radius <= 180: ')
minmagnitude = input('Enter min magnitude:')


url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
response = requests.get(url, headers={'Accept': 'application/json'}, params={
	'format': 'geojson',
	'starttime': starttime,
	'endtime': endtime,
	'latitude': latitude,
	'longitude': longitude,
	'maxradius': maxradius,
	'minmagnitude': minmagnitude
	})


earthquake_list = []


data = response.json()
new_data = data['features']
for earhquake in new_data:
	earthquake_list.append([earhquake['properties']['place'], earhquake['properties']['mag']])




def writing_to_csv(list):
	with open('earthquakes.csv', 'w', encoding='utf-8') as file:
		headers_earhquake = ['Place', 'Magnitude']
		csv_writer = csv.DictWriter(file, fieldnames=headers_earhquake)
		csv_writer.writeheader()
		for earthquake in list:
			csv_writer.writerow({
				'Place': earthquake[0],
				'Magnitude': earthquake[1]
				})


writing_to_csv(earthquake_list)



def reader_csv():
	try:
		with open('earthquakes.csv') as file:
			csv_reader = csv.DictReader(file)
			for earthquake in csv_reader:
				print('Place: {}. Magnitude: {}'.format(earthquake['Place'], earthquake['Magnitude']))
	except:
		print('File earthquakes.csv are not create.')


reader_csv()