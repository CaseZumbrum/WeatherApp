#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests, json
import logging
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import os
import time

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

def K_to_F(K):
    return (K - 273.15) * 9 / 5 + 32


def getweather():
    current = response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?appid=e91b4794a9aac2f29d302a924907e5ac&q=Gainesville").json()
    Forecast = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast?lat=29.6520&lon=-82.3250&appid=e91b4794a9aac2f29d302a924907e5ac").json()
    info = {}
    info["currtemp"] = round(K_to_F(current["main"]["temp"]))
    info["currkind"] = current["weather"][0]["description"]
    info["currhumidity"] = current["main"]["humidity"]
    info["high"] = round(K_to_F(current["main"]["temp_max"]))
    info["low"] = round(K_to_F(current["main"]["temp_min"]))
    info["rain"] = [0, 0]
    for i in range(3):
        id = Forecast["list"][i]["weather"][0]["id"]
        if id // 100 == 2 or id // 100 == 3 or id // 100 == 5:
            info["rain"][0] = 1
            info["rain"][1] = round((Forecast["list"][i]["dt"] / (3600)) - time.time() / 3600)
            break

    return info


def printscreen(info):
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("epd7in5_V2 Demo")
        epd = epd7in5_V2.EPD()
        epd.init()
       
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 50)
        

        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 10), f'Current temp: {info["currtemp"]}', font = font24, fill = 0)
        draw.text((10, 60), f'{info["currkind"]}', font = font24, fill = 0)
        draw.text((10, 110), f'High: {info["high"]}', font = font24, fill = 0)
        draw.text((10, 160), f'Low: {info["low"]}', font = font24, fill = 0)
        draw.text((10, 210), f'Humidity: {info["currhumidity"]}', font=font24, fill=0)

        if(info["rain"][0] == 1):
            draw.text((10, 260), f'Chance of rain in about {info["rain"][1]} hours', font = font24, fill = 0)

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

if __name__ ==  "__main__":
    try:
        info = getweather()
        printscreen(info)
        while(True):
            info = getweather()

            time215minute = (60*15) - time.time()%(60*15)
            print(f"Waiting for {time215minute}")
            time.sleep(time215minute)
            
            printscreen(info)

    except KeyboardInterrupt:   
        logging.info("ctrl + c:")
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()
        time.sleep(2)
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        exit()