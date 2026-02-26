import pkg_resources, subprocess, sys
import csv
from datetime import date
from datetime import datetime
from datetime import timedelta

required  = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

import requests

csv_file1 = "/config/www/ocppexport1.txt"
csv_file2 = "/config/www/ocppexport2.txt"
url = 'http://homeassistant.local:8123/api/states/sensor.'
days = int(date.today().strftime("%d"))

headers = {
    'Authorization': 'Bearer TOKEN',
    'content-type': 'application/json'
}

# Read the csv_file
csv_reader1 = csv.DictReader(open(csv_file1), delimiter=';')

the_list1 = []
kwh_list1 = []

for line in csv_reader1:
    tempdate = datetime.strptime(line['date'], '%d.%m.%Y')
    deltaMonth = timedelta(days=int(date.today().strftime("%d")))
    deltaToday = date.today() - tempdate.date()
    if deltaToday < deltaMonth:
        the_list1.append(line)
        kwh_list1.append(float(line['charged']))

# Revert the list, we want the last row at the top
the_list1.reverse()
kwh_list1.reverse()

# Read the csv_file
csv_reader2 = csv.DictReader(open(csv_file2), delimiter=';')

the_list2 = []
kwh_list2 = []

for line in csv_reader2:
    tempdate = datetime.strptime(line['date'], '%d.%m.%Y')
    deltaMonth = timedelta(days=int(date.today().strftime("%d")))
    deltaToday = date.today() - tempdate.date()
    if deltaToday < deltaMonth:
        the_list2.append(line)
        kwh_list2.append(float(line['charged']))

# Revert the list, we want the last row at the top
the_list2.reverse()
kwh_list2.reverse()

errors = ''

variable1 = 'ocpp1_energy'
variable2 = 'ocpp2_energy'
attributes1 = '{"unit_of_measurement": "kWh", "device_class": "energy", "friendly_name": "Daniel", "entries": ' + str(the_list1) + '}'
attributes2 = '{"unit_of_measurement": "kWh", "device_class": "energy", "friendly_name": "Andere", "entries": ' + str(the_list2) + '}'

data1 = '{"state": "' + str(sum(kwh_list1)) + '", "attributes": ' + attributes1 + '}'
data1 = data1.replace("'",'"')

data2 = '{"state": "' + str(sum(kwh_list2)) + '", "attributes": ' + attributes2 + '}'
data2 = data2.replace("'",'"')

r1 = requests.post(url+variable1, data=data1, headers=headers)
if r1.status_code != 200 and r1.status_code != 201:
    errors = errors + 'ERROR:' + variable1 + ' - ' + str(r1.status_code)

r2 = requests.post(url+variable2, data=data2, headers=headers)
if r2.status_code != 200 and r2.status_code != 201:
    errors = errors + 'ERROR:' + variable2 + ' - ' + str(r2.status_code)

if errors != '':
    print(errors)
