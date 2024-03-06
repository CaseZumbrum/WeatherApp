
import network
import urequests
import json
import framebuf
import time
from EPD_7in5 import EPD_7in5
from machine import Pin, SPI
from writer import Writer
import FreeSans50  # Font to use
from random import choice, randint
#import ntptime



def K_to_F(K):
    return (K - 273.15) * 9 / 5 + 32

def getweather():
    current = json.loads(urequests.get(
        "http://api.openweathermap.org/data/2.5/weather?appid=e91b4794a9aac2f29d302a924907e5ac&q=Gainesville").text)
    Forecast = json.loads(urequests.get(
        "http://api.openweathermap.org/data/2.5/forecast?lat=29.6520&lon=-82.3250&appid=e91b4794a9aac2f29d302a924907e5ac").text)

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
            info["rain"][1] = round((Forecast["list"][i]["dt"] / (3600)) -time.time() / 3600)
            break

    randomevent = [f'fog: yes', "fog: no", f"Days Left: {randint(0, 1000)}",
                   f"Hot single moms {randint(0, 1000)} meters away!", "Nick is hiding somewhere.",
                   "Don't forget to change your mind!", "WAKE UP", "Meeting with Mr. Peabody",
                   "Head?"]
    info["random"] = choice(randomevent)
    return info


def printscreen(info):
    try:
        
        epd = EPD_7in5()
        wri = Writer(epd, FreeSans50, verbose = False)  # verbose = False to suppress console output
        
        epd.fill(0x00)
        Writer.set_textpos(epd, 10, 10)
        wri.printstring('Current temp: ' + str(info["currtemp"]))
        Writer.set_textpos(epd, 60, 10)
        wri.printstring(str(info["currkind"]))
        Writer.set_textpos(epd, 110, 10)
        wri.printstring('High: ' + str(info["high"]))
        Writer.set_textpos(epd, 160, 10)
        wri.printstring('Low: ' + str(info["low"]))
        Writer.set_textpos(epd, 210, 10)
        wri.printstring('Humidity: ' + str(info["currhumidity"]))
        Writer.set_textpos(epd, 400, 10)
        wri.printstring(str(info["random"]))
        
        Writer.set_textpos(epd, 300, 10)
        wri.printstring(str(time.time()))
        
        
        if(info["rain"][0] == 1):
            Writer.set_textpos(epd, 260, 10)
            wri.printstring('Chance of ' + str(info["rain"][2]) + "rain in about " + str(info["rain"][1]) + " hours")
        
        epd.display(epd.buffer)
        epd.delay_ms(2000)
        epd.sleep()
        
    except KeyboardInterrupt:
        epd.Clear()
        epd.delay_ms(2000)
        print("sleep")
        epd.sleep()



        
if __name__=='__main__':
    time.sleep(10)
    led = Pin("LED", machine.Pin.OUT)
    
        
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("ufdevice", "gogators")
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(3)
        wlan.connect("ufdevice", "gogators")
    print("Wifi Connected")
    
    try:
        #ntptime.settime()
        info = getweather()
        printscreen(info)
        
    
        while (True):
            info = getweather()
            time215minute = (60 * 15) - time.time() % (60 * 15)
            print("Waiting for " + str(time215minute))
            time.sleep(time215minute)
            printscreen(info)
            
    except KeyboardInterrupt:
        epd = EPD_7in5()
        wri = Writer(epd, FreeSans50, verbose = False)  # verbose = False to suppress console output
        epd.Clear()
        epd.delay_ms(2000)
        print("sleep")
        epd.sleep()
    except Exception as e:
        
        f = open("test.txt", "a")
 
        # writing in the file
        f.write(str(e) + "\n")
         
        # closing the file
        f.close()
        led.on()
        time.sleep(5)
        led.off()
        
    finally:
        print("done")
        pass
            
    
    
         




