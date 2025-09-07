#!/bin/python

import pkg_resources, sqlite3, subprocess, sys, time
from datetime import datetime
from datetime import timedelta

required  = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

import requests

# Local Home Assistant API access URL
url = 'http://homeassistant.local:8123/api/states/sensor.'

# The one and only... long lasting token!
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyZmI3Nzg3OTEwNDE0NTZkYWNlMzExMWVkYmUxMjhiNyIsImlhdCI6MTY5NzM2Nzg1OSwiZXhwIjoyMDEyNzI3ODU5fQ.05mfSBnhZm0LxBdEZOBEjDU3OKHI7A0iNmecYhznY1Y',
    'content-type': 'application/json'
}

# Some dates and math for the steps sensor
today = datetime.now()

startDay = today.strftime('%Y-%m-%d 00:00:00')
startDayX = time.mktime(datetime.strptime(startDay, "%Y-%m-%d %H:%M:%S").timetuple())

endDay = today.strftime('%Y-%m-%d 23:59:59')
endDayX = time.mktime(datetime.strptime(endDay, "%Y-%m-%d %H:%M:%S").timetuple())

# SQLite database location
db_path = "/media/Drive/Gadgetbridge.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQLite query to retrieve the total steps for the current day and put this into a variable
steps_query = f"SELECT SUM(STEPS) as Steps FROM KEEP_FIT_ACTIVITY_SAMPLE WHERE TIMESTAMP BETWEEN {startDayX} AND {endDayX};"
cursor.execute(steps_query)
daily_steps = int(cursor.fetchone()[0] or 0)

print("Daily steps data has been saved: " + str(daily_steps))

# SQLite query to retrieve the most recent heart rate value and put this into a variable
heart_rate_query = f"SELECT HEART_RATE FROM KEEP_FIT_HEART_RATE_SAMPLE WHERE TIMESTAMP ORDER BY TIMESTAMP DESC;"
cursor.execute(heart_rate_query)
try:
    current_heart_rate = int(cursor.fetchone()[0] or 0)
except:
    current_heart_rate = 0

print("Current heart rate data has been saved: " + str(current_heart_rate))

# SQLite query to retrieve the most recent heart rate value and put this into a variable
spo2_query = f"SELECT SPO2 FROM KEEP_FIT_SPO2_SAMPLE WHERE TIMESTAMP ORDER BY TIMESTAMP DESC;"
cursor.execute(spo2_query)
try:
    current_spo2 = int(cursor.fetchone()[0] or 0)
except:
    current_spo2 = 0

print("Current spo2 data has been saved: " + str(current_spo2))

# SQLite query to retrieve the most recent stress value and put this into a variable
stress_query = f"SELECT STRESS FROM KEEP_FIT_STRESS_SAMPLE WHERE TIMESTAMP ORDER BY TIMESTAMP DESC;"
cursor.execute(stress_query)
try:
    current_stress = int(cursor.fetchone()[0] or 0)
except:
    current_stress = 0

print("Current stress level data has been saved: " + str(current_stress))

# SQLite query to retrieve the most recent diastolic blood pressure value and put this into a variable
bp_diastolic_query = f"SELECT BP_DIASTOLIC FROM KEEP_FIT_BLOOD_PRESSURE_SAMPLE WHERE TIMESTAMP ORDER BY TIMESTAMP DESC;"
cursor.execute(bp_diastolic_query)
try:
    current_bp_diastolic = int(cursor.fetchone()[0] or 0)
except:
    current_bp_diastolic = 0
    
print("Current diastolic blood pressure data has been saved: " + str(current_bp_diastolic))

# SQLite query to retrieve the most recent systolic blood pressure value and put this into a variable
bp_systolic_query = f"SELECT BP_SYSTOLIC FROM KEEP_FIT_BLOOD_PRESSURE_SAMPLE WHERE TIMESTAMP ORDER BY TIMESTAMP DESC;"
cursor.execute(bp_systolic_query)
try:
    current_bp_systolic = int(cursor.fetchone()[0] or 0)
except:
    current_bp_systolic = 0

print("Current systolic blood pressure data has been saved: " + str(current_bp_systolic))

# SQLite query to retrieve the most recent sleep score value and put this into a variable
sleep_score_query = f"SELECT SLEEP_SCORE FROM KEEP_FIT_SLEEP_SAMPLE WHERE TIMESTAMP ORDER BY TIMESTAMP DESC;"
cursor.execute(sleep_score_query)
try:
    current_sleep_score = int(cursor.fetchone()[0] or 0)
except:
    current_sleep_score = 0

print("Current sleep score data has been saved: " + str(current_sleep_score))

# SQLite query to retrieve the most recent battery level value and put this into a variable
battery_level_query = f"SELECT LEVEL FROM BATTERY_LEVEL WHERE TIMESTAMP ORDER BY TIMESTAMP DESC;"
cursor.execute(battery_level_query)
try:
    current_battery_level = int(cursor.fetchone()[0] or 0)
except:
    current_battery_level = 0

print("Current battery level data has been saved: " + str(current_battery_level))

# SQLite query to retrieve data about the gadget and put them into variables
device_name_query = f"SELECT NAME FROM DEVICE;"
cursor.execute(device_name_query)
try:
    device_name = cursor.fetchone()[0]
except:
    device_name = "None"

device_type_query = f"SELECT TYPE_NAME FROM DEVICE;"
cursor.execute(device_type_query)
try:
    device_type = cursor.fetchone()[0]
except:
    device_type = "None"

device_manufacturer_query = f"SELECT MANUFACTURER FROM DEVICE;"
cursor.execute(device_manufacturer_query)
try:
    device_manufacturer = cursor.fetchone()[0]
except:
    device_manufacturer = "None"

device_identifier_query = f"SELECT IDENTIFIER FROM DEVICE;"
cursor.execute(device_identifier_query)
try:
    device_identifier = cursor.fetchone()[0]
except:
    device_identifier = "None"

device_firmware_query = f"SELECT FIRMWARE_VERSION1 FROM DEVICE_ATTRIBUTES ORDER BY _id DESC;"
cursor.execute(device_firmware_query)
temp_fw_ver = cursor.fetchall()

if (temp_fw_ver[0])[0] =='':
    device_firmware = (temp_fw_ver[0])[1]
else:
    device_firmware = (temp_fw_ver[0])[0]

print("Current device data has been saved. Name: " + str(device_name) + ", Type: " + str(device_type) + ", Manufacturer: " + str(device_manufacturer) + ", Identifier: " + str(device_identifier) + ", Firmware: " + str(device_firmware))

# After all data is extracted, close the connection to the database again
conn.close()

# Get the extracted data into Home Assistant
errors = ''

# sensor names
variable1 = 'ring_schritte_heute'
variable2 = 'ring_puls'
variable3 = 'ring_spo2'
variable4 = 'ring_stresswert'
variable5 = 'ring_blutdruck_systolisch'
variable6 = 'ring_blutdruck_diastolisch'
variable7 = 'ring_schlafwert'
variable8 = 'ring_batterie'
variable9 = 'ring_geraet'

attributes1 = '{"unit_of_measurement": "steps", "state_class": "total_increasing", "friendly_name": "Ring Schritte heute", "icon": "mdi:walk"}'
attributes2 = '{"unit_of_measurement": "bpm", "state_class": "measurement", "friendly_name": "Ring Puls", "icon": "mdi:heart-pulse"}'
attributes3 = '{"unit_of_measurement": "%", "state_class": "measurement", "friendly_name": "Ring SpO2", "icon": "mdi:water-plus"}'
attributes4 = '{"friendly_name": "Ring Stresswert", "icon": "mdi:pulse"}'
attributes5 = '{"unit_of_measurement": "mmHg", "device_class": "pressure", "friendly_name": "Ring systolischer Blutdruck", "icon": "mdi:heart-pulse"}'
attributes6 = '{"unit_of_measurement": "mmHg", "device_class": "pressure", "friendly_name": "Ring diastolischer Blutdruck", "icon": "mdi:heart-pulse"}'
attributes7 = '{"friendly_name": "Ring Schlafwert", "icon": "mdi:sleep"}'
attributes8 = '{"unit_of_measurement": "%", "state_class": "measurement", "device_class": "battery", "friendly_name": "Ring Batteriestand", "icon": "mdi:battery"}'
attributes9 = '{"device_name": "' + str(device_name) + '", "device_type": "' + str(device_type) + '", "device_manufacturer": "' + str(device_manufacturer) + '", "device_identifier": "' + str(device_identifier) + '", "device_firmware": "' + str(device_firmware) + '", "friendly_name": "Ring Geräteinformationen", "icon": "mdi:devices"}'

# Prepare the data
data1 = '{"state": "' + str(daily_steps) + '", "attributes": ' + attributes1 + '}'
data1 = data1.replace("'",'"')
data2 = '{"state": "' + str(current_heart_rate) + '", "attributes": ' + attributes2 + '}'
data2 = data2.replace("'",'"')
data3 = '{"state": "' + str(current_spo2) + '", "attributes": ' + attributes3 + '}'
data3 = data3.replace("'",'"')
data4 = '{"state": "' + str(current_stress) + '", "attributes": ' + attributes4 + '}'
data4 = data4.replace("'",'"')
data5 = '{"state": "' + str(current_bp_systolic) + '", "attributes": ' + attributes5 + '}'
data5 = data5.replace("'",'"')
data6 = '{"state": "' + str(current_bp_diastolic) + '", "attributes": ' + attributes6 + '}'
data6 = data6.replace("'",'"')
data7 = '{"state": "' + str(current_sleep_score)  + '", "attributes": ' + attributes7 + '}'
data7 = data7.replace("'",'"')
data8 = '{"state": "' + str(current_battery_level) + '", "attributes": ' + attributes8 + '}'
data8 = data8.replace("'",'"')
data9 = '{"state": "' + str(device_name) + '", "attributes": ' + attributes9 + '}'
data9 = data9.replace("'",'"')

# Get data into sensors via API
r1 = requests.post(url+variable1, data=data1, headers=headers)
if r1.status_code != 200 and r1.status_code != 201:
    errors = errors + 'ERROR:' + variable1 + ' - ' + str(r1.status_code)

r2 = requests.post(url+variable2, data=data2, headers=headers)
if r2.status_code != 200 and r2.status_code != 201:
    errors = errors + 'ERROR:' + variable2 + ' - ' + str(r2.status_code)

r3 = requests.post(url+variable3, data=data3, headers=headers)
if r3.status_code != 200 and r3.status_code != 201:
    errors = errors + 'ERROR:' + variable3 + ' - ' + str(r3.status_code)

r4 = requests.post(url+variable4, data=data4, headers=headers)
if r4.status_code != 200 and r4.status_code != 201:
    errors = errors + 'ERROR:' + variable4 + ' - ' + str(r4.status_code)

r5 = requests.post(url+variable5, data=data5, headers=headers)
if r5.status_code != 200 and r5.status_code != 201:
    errors = errors + 'ERROR:' + variable5 + ' - ' + str(r5.status_code)

r6 = requests.post(url+variable6, data=data6, headers=headers)
if r6.status_code != 200 and r6.status_code != 201:
    errors = errors + 'ERROR:' + variable6 + ' - ' + str(r6.status_code)

r7 = requests.post(url+variable7, data=data7, headers=headers)
if r7.status_code != 200 and r7.status_code != 201:
    errors = errors + 'ERROR:' + variable7 + ' - ' + str(r7.status_code)

r8 = requests.post(url+variable8, data=data8, headers=headers)
if r8.status_code != 200 and r8.status_code != 201:
    errors = errors + 'ERROR:' + variable8 + ' - ' + str(r8.status_code)

r9 = requests.post(url+variable9, data=data9, headers=headers)
if r9.status_code != 200 and r9.status_code != 201:
    errors = errors + 'ERROR:' + variable9 + ' - ' + str(r9.status_code)
