# Mixed-HomeAssistant-stuff
My mixed additions to my How Assistant Setup. These are the more complex ones

* [GadgetBridge Integration](#gadgetbridge)
* [OCPP Sensors for charge costs](#ocpp)

### <a name="gadgetbridge"></a>GadgetBridge Integration
My ... complicated way to get all data from my smart ring into my Home Asisstant Setup.

1. You need your won way to send the most recent database to a location where your Home Assistant can find it. I installed Synology Drive on my phone for that and by that save the database into my Drive and this folder can be accessed from HA as SMB share, too. Just set it up as media share in the HA settings and you can grab the most recent file from there.

2. Enable the intent features of GadgetBridge so that you can control the app via HA automations.
3. Enable the auto export of the database. Here you can send the file to Synology Drive for example. The value on how often is quite irrelevant here as we use intent broadcasts to get the file way more often than this setting would allow.
4. Integrate the sensors and automations into your HA installation.
5. PROFIT!

<p align="center">
  <img src="https://raw.githubusercontent.com/dreimer1986/Mixed-HomeAssistant-stuff/master/images/GadgetBridge.png">
</p>

### <a name="ocpp"></a>OCPP Sensors for charge costs
Long story... I need to pay for my charges on my wallbox to my parents. The only way I was allowed to use Home Assistant for the cost calculation was to output the raw data as CSV, too. And thus this little monster was born. I save the data to a CSV and get my data from there again, too.

Most important thing for this of course is this Addon from HACS: https://github.com/lbbrhzn/ocpp

IMPORTANT! Edit the first line of the CSV files when they got created:

```
date;time;sessiontime;token;charged
```
That way it's a real and valid CSV file.

Add the dummy sensors and the automations to your HA setup, too.

<p align="center">
  <img src="https://raw.githubusercontent.com/dreimer1986/Mixed-HomeAssistant-stuff/master/images/OCPP.png">
</p>
