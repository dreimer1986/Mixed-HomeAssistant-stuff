#!/usr/bin/env python3
import os
import sqlite3
import json
import sys
import requests

url = 'http://homeassistant.local:8123/api/states/sensor.'
headers = {
    'Authorization': 'Bearer TOKEN',
    'content-type': 'application/json'
}

db_path = "/config/DHouseFit_plain.db"
if not os.path.exists(db_path):
    print(f"Datenbank unter {db_path} nicht gefunden!")
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def safe_query(query, default_val=0, is_int=True):
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        if row and row[0] is not None:
            return int(row[0]) if is_int else str(row[0])
        return default_val
    except Exception as e:
        print(f"Query-Fehler: {e}")
        return default_val

# Beispielhafte Datenextraktion (erweitere dies um deine spezifischen Queries)
daily_steps = safe_query("SELECT total_step FROM t_data_step ORDER BY date DESC LIMIT 1;", 0)
daily_calorie = safe_query("SELECT calorie FROM t_data_step ORDER BY date DESC LIMIT 1;", 0) / 1000
daily_distance = safe_query("SELECT distance FROM t_data_step ORDER BY date DESC LIMIT 1;", 0) / 1000
current_pulse = safe_query("SELECT avg_hr FROM t_data_hr ORDER BY date DESC LIMIT 1;", 0)
current_spo2 = safe_query("SELECT avg_bo FROM t_data_bo ORDER BY date DESC LIMIT 1;", 0)
current_sleep_total = safe_query("SELECT total_sleep_time FROM t_data_sleep ORDER BY date DESC LIMIT 1;", 0)
current_sleep_deep = safe_query("SELECT sleep_deep_time FROM t_data_sleep ORDER BY date DESC LIMIT 1;", 0)
current_sleep_light = safe_query("SELECT sleep_light_time FROM t_data_sleep ORDER BY date DESC LIMIT 1;", 0)
current_sleep_rapid = safe_query("SELECT sleep_rapid_time FROM t_data_sleep ORDER BY date DESC LIMIT 1;", 0)
current_wake_up_count = safe_query("SELECT wake_up_count FROM t_data_sleep ORDER BY date DESC LIMIT 1;", 0)

user_name = safe_query("SELECT NAME FROM t_user LIMIT 1;", "Unbekannt", is_int=False)
user_birthday = safe_query("SELECT BIRTHDAY FROM t_user LIMIT 1;", "Unbekannt", is_int=False)
user_gender = safe_query("SELECT SEX FROM t_user LIMIT 1;", "Unbekannt", is_int=False)
user_weight = safe_query("SELECT WEIGHT FROM t_user LIMIT 1;", 0)
user_height = safe_query("SELECT HEIGHT FROM t_user LIMIT 1;", 0)
user_steps = safe_query("SELECT steps_target FROM t_user LIMIT 1;", 10000)
user_account = safe_query("SELECT ACCOUNT FROM t_user LIMIT 1;", "Kein Account", is_int=False)

conn.close()

sensors = {
    'ring_schritte_heute': {
        'state': daily_steps,
        'attributes': {"unit_of_measurement": "steps", "state_class": "measurement", "friendly_name": "Ring Schritte heute", "icon": "mdi:walk"}
    },
    'ring_kalorien_heute': {
        'state': daily_calorie,
        'attributes': {"unit_of_measurement": "kcal", "state_class": "measurement", "friendly_name": "Ring Kalorien heute", "icon": "mdi:walk"}
    },
    'ring_distanz_heute': {
        'state': daily_distance,
        'attributes': {"unit_of_measurement": "km", "state_class": "measurement", "friendly_name": "Ring Distanz heute", "icon": "mdi:walk"}
    },
    'ring_puls': {
        'state': current_pulse,
        'attributes': {"unit_of_measurement": "bpm", "state_class": "measurement", "friendly_name": "Ring Puls", "icon": "mdi:heart-pulse"}
    },
    'ring_spo2': {
        'state': current_spo2,
        'attributes': {"unit_of_measurement": "%", "state_class": "measurement", "friendly_name": "Ring SpO2-Wert", "icon": "mdi:water-percent"}
    },
    'ring_allg_schlaf': {
        'state': current_sleep_total,
        'attributes': {"unit_of_measurement": "min", "state_class": "measurement", "friendly_name": "Ring allg. Schlafwert", "icon": "mdi:sleep"}
    },
    'ring_tief_schlaf': {
        'state': current_sleep_deep,
        'attributes': {"unit_of_measurement": "min", "state_class": "measurement", "friendly_name": "Ring Tiefschlafwert", "icon": "mdi:sleep"}
    },
    'ring_leicht_schlaf': {
        'state': current_sleep_light,
        'attributes': {"unit_of_measurement": "min", "state_class": "measurement", "friendly_name": "Ring leichter Schlafwert", "icon": "mdi:sleep"}
    },
    'ring_rapid_schlaf': {
        'state': current_sleep_rapid,
        'attributes': {"unit_of_measurement": "min", "state_class": "measurement", "friendly_name": "Ring REM-Schlafwert", "icon": "mdi:sleep"}
    },
    'ring_wakeup': {
        'state': current_wake_up_count,
        'attributes': {"state_class": "measurement", "friendly_name": "Ring Aufgewacht-Wert", "icon": "mdi:sleep-off"}
    },
    'ring_benutzer': {
        'state': user_name,
        'attributes': {
            "user_birthday": user_birthday, "user_gender": user_gender, "user_weight": user_weight, "user_height": user_height,
            "user_steps": user_steps, "user_account": user_account, "friendly_name": "Ring Benutzerinformationen", "icon": "mdi:account"
        }
    }
}

for sensor_name, payload in sensors.items():
    response = requests.post(f"{url}{sensor_name}", headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Fehler bei {sensor_name}: {response.status_code}")
