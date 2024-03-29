#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import requests, json
import logging
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import os
import time
import random

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)


def K_to_F(K):
    return (K - 273.15) * 9 / 5 + 32


def getweather():
    current = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?appid=e91b4794a9aac2f29d302a924907e5ac&q=Gainesville").json()
    Forecast = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast?lat=29.6520&lon=-82.3250&appid=e91b4794a9aac2f29d302a924907e5ac").json()

    info = {}
    info["currtemp"] = round(K_to_F(current["main"]["temp"]))
    info["currkind"] = current["weather"][0]["description"][0].upper() + current["weather"][0]["description"][1:]
    info["currhumidity"] = current["main"]["humidity"]
    info["icon"] = current["weather"][0]["icon"]
    info["high"] = round(K_to_F(current["main"]["temp_max"]))
    info["low"] = round(K_to_F(current["main"]["temp_min"]))
    info["rain"] = [0, 0, ""]

    for i in range(3):
        id = Forecast["list"][i]["weather"][0]["id"]
        if id // 100 == 2 or id // 100 == 3 or id // 100 == 5:

            if id // 100 == 2:
                info["rain"][2] = "heavy "
            elif id // 100 == 3:
                info["rain"][2] = "light "

            info["rain"][0] = 1
            info["rain"][1] = round((Forecast["list"][i]["dt"] / (3600)) - time.time() / 3600)
            break

    randomevent = [f'fog: yes', "fog: no", f"Days Left: {random.randint(0, 1000)}",
                   f"Hot single moms {random.randint(0, 1000)} meters away!", "Nick is hiding somewhere.",
                   "Don't forget to change your mind today!", "WAKE UP", "Meeting with Mr. Peabody today at 4:00",
                   "Head?"]
    info["random"] = random.choice(randomevent)
    return info


def printscreen(info):
    logging.basicConfig(level=logging.DEBUG)

    try:

        epd = epd7in5_V2.EPD()
        epd.init()

        test_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 50)

        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 10), f'Current temp: {info["currtemp"]}', font=test_font, fill=0)
        draw.text((10, 60), f'{info["currkind"]}', font=test_font, fill=0)
        draw.text((10, 110), f'High: {info["high"]}', font=test_font, fill=0)
        draw.text((10, 160), f'Low: {info["low"]}', font=test_font, fill=0)
        draw.text((10, 210), f'Humidity: {info["currhumidity"]}', font=test_font, fill=0)
        draw.text((10, 400), info["random"], font=test_font, fill=0)

        if (info["rain"][0] == 1):
            draw.text((10, 260), f'Chance of {info["rain"][2]}rain in about {info["rain"][1]} hours', font=test_font,
                      fill=0)

        img = Image.open(requests.get(f"https://openweathermap.org/img/wn/{info['icon']}@2x.png", stream=True).raw)
        img = img.resize((200, 200))
        Himage.paste(img, (500, 20))

        epd.display(epd.getbuffer(Himage))
        time.sleep(2)
        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()
        time.sleep(2)
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        exit()


if __name__ == "__main__":
    try:
        info = getweather()
        printscreen(info)
        while (True):
            info = getweather()

            time215minute = (60 * 15) - time.time() % (60 * 15)
            print(f"Waiting for {time215minute}")
            time.sleep(time215minute)

            printscreen(info)

    except KeyboardInterrupt:
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()
        time.sleep(2)
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        exit()
