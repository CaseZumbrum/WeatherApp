# import the module
import python_weather
from datetime import datetime
import asyncio
import os


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
            print(hourly.time.hour)
            if(now.hour < hourly.time.hour):
                if "Showers" in str(hourly.kind):
                    info["rain"] = (1,hourly.time.hour - now.hour)
                    break


        print(info)
'''
        # get the weather forecast for a few days
        for forecast in weather.forecasts:
            print(forecast)

            # hourly forecasts
            for hourly in forecast.hourly:
                print(f' --> {hourly!r}')
                '''


if __name__ == '__main__':
    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(getweather())