# Mixed-HomeAssistant-stuff
My mixed additions to my Home Assistant Setup. These are the more complex ones

* [GadgetBridge Integration](#gadgetbridge)
* [OCPP Sensors for charge costs](#ocpp)

The ePaper stuff can be found here: https://github.com/dreimer1986/openePaperLink-Stuff

And YES, the anime backgrounds are no still images, they are animated all over HA: https://github.com/dreimer1986/yourname_card_mod

### <a name="gadgetbridge"></a>GadgetBridge Integration
My ... complicated way to get all data from my smart ring into my Home Asisstant Setup.

1. You need your own way to send the most recent database to a location where your Home Assistant can find it. I installed Synology Drive on my phone for that and by that I can easily save the database into my Drive and this folder can be accessed from HA as SMB share, too. Just set it up as Media Share in the HA settings and you can grab the most recent file from there.

2. Enable the intent features of GadgetBridge under Developer Settings so that you can control the app via HA automations.
3. Enable the auto export of the database. Here you can send the file to Synology Drive for example. The value on how often is quite irrelevant here as we use intent broadcasts to get the file way more often than this setting would allow.
4. Move the Python script into your "homeassistant" folder.
5. Integrate the sensors and automations into your HA installation. Yes, it works without these dummy sensors, but then the sensors are reset to ZERO including the history data on every reboot of HA. Thus these sensors are just here to make the data last after a reboot.
6. PROFIT!

<p align="center">
  <img src="https://raw.githubusercontent.com/dreimer1986/Mixed-HomeAssistant-stuff/master/images/GadgetBridge.png">
</p>

### <a name="ocpp"></a>OCPP Sensors for charge costs
Long story... I need to pay for my charges on my wallbox to my parents. The only way I was allowed to use Home Assistant for the cost calculation was to output the raw data as CSV, too. Why you ask? Because my family wants to be able to get the data for their own little projects my IT crazy brothers made up. And thus this little monster was born. I save the data to a CSV and get my data from there again, too.

Most important thing for this of course is this Addon from HACS: https://github.com/lbbrhzn/ocpp

IMPORTANT! Edit the first line of the CSV files when they got created:

```
date;time;sessiontime;token;charged
```
That way it's a real and valid CSV file. Before that the 1st line is just some useless information HA added to it.

Move the python script into "homeassistant" folder and add the dummy sensors and automations to your HA setup, too. Same reason for the dummy sensors as you saw above.

And we need a helper in form of a input_number: input_number.energy_cost which needs to be filled with the price/kWh to make the calculations work at all. It must be filled with € and not ct. Thus I have "0.3" in there right now.

<p align="center">
  <img src="https://raw.githubusercontent.com/dreimer1986/Mixed-HomeAssistant-stuff/master/images/OCPP.png">
</p>
