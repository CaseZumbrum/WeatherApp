#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import python_weather
from datetime import datetime
import asyncio
import os
import time


async def getweather():
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        now = datetime.now()
        weather = await client.get('Gainesville')
        info = {}
        forecast = next(weather.forecasts)
        # returns the current day's forecast temperature (int)
        info["currtemp"] = weather.current.temperature
        info['currkind'] = str(weather.current.kind)
        info['high'] = forecast.highest_temperature
        info['low'] = forecast.lowest_temperature
        info["rain"] = (0,0)
        for hourly in forecast.hourly:
            print(hourly)
            if(now.hour < hourly.time.hour):
                if "Showers" in str(hourly.kind):
                    info["rain"] = (1,hourly.time.hour - now.hour)
                    break
        return info



def printscreen(info):
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("epd7in5_V2 Demo")
        epd = epd7in5_V2.EPD()
        epd.init()
        '''
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(2)
        '''
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 50)
        

        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 10), f'Current temp: {info["currtemp"]}', font = font24, fill = 0)
        draw.text((10, 60), f'{info["currkind"]}', font = font24, fill = 0)
        draw.text((10, 110), f'High: {info["high"]}', font = font24, fill = 0)
        draw.text((10, 160), f'Low: {info["low"]}', font = font24, fill = 0)
        if(info["rain"][0] == 1):
            draw.text((10, 210), f'Chance of rain in {info["rain"][1]} hours', font = font24, fill = 0)
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
        hour = datetime.now().hour
        info = asyncio.run(getweather())
        printscreen(info)
        while(True):
            info = asyncio.run(getweather())
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