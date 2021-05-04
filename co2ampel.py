import json
import os
import requests
import sys
import time
import yaml


def set_led_color(led_id, led_color):
    try:
        led_state = requests.get(f"http://{config['bridge']['ip']}/api/{config['bridge']['username']}/lights/{led_id}").json()
        led_color_before = led_state["state"]["hue"]
    except:
        led_color_before = led_color
        pass

    try:
        led_data = {
            "on": True, 
            "bri": config["led_bri"], 
            "sat": config["led_sat"],
            "hue": led_color 
        }

        requests.put(f"http://{config['bridge']['ip']}/api/{config['bridge']['username']}/lights/{led_id}/state", data=json.dumps(led_data))

        if led_color != led_color_before:
            time.sleep(1)
            led_data["alert"] = "lselect"
            requests.put(f"http://{config['bridge']['ip']}/api/{config['bridge']['username']}/lights/{led_id}/state", data=json.dumps(led_data))
    except:
        pass


def main():
    try:
        auth_data = {
            "grant_type": "password",
            "scope": "read_station",
            "client_id": config["netatmo"]["client_id"],
            "client_secret": config["netatmo"]["client_secret"],
            "username": config["netatmo"]["username"],
            "password": config["netatmo"]["password"]
        }

        ws_auth = requests.post("https://api.netatmo.com/oauth2/token", data=auth_data).json()

        access_token = { 
            "access_token": ws_auth["access_token"]
        }

        ws_data = requests.post("https://api.netatmo.net/api/getstationsdata", data=access_token).json()
    except:
        for r in config["rooms"]:
            room = config["rooms"][r]
            set_led_color(room["led_id"], config["led_error"])

        print("Netatmo API error! Exiting...")

        sys.exit(1)

    for r in config["rooms"]:
        room = config["rooms"][r]

        for module in ws_data["body"]["devices"][0]["modules"]:
            if module["_id"] == room["sensor_id"]:
                try:
                    co2 = int(module["dashboard_data"].get("CO2"))
                except:
                    co2 = 0
                    pass

                print(f"{r}: {co2}ppm")

                if co2 <= 0:
                    led_color = config["led_error"]
                elif co2 > 0 and co2 < config["ppm_warning"]:
                    led_color = config["led_ok"]
                elif co2 >= config["ppm_warning"] and co2 < config["ppm_alert"]:
                    led_color = config["led_warning"]
                else:
                    led_color = config["led_alert"]

                set_led_color(room["led_id"], led_color)


if __name__ == "__main__":
    try:
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/config.yml", "r") as f:
            config = yaml.safe_load(f)
    except:
        print("Config Error! Exiting...")
        sys.exit(1)

    main()
