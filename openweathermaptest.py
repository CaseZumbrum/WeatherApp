# import required modules
import requests, json

'''
# Enter your API key here
api_key = "e91b4794a9aac2f29d302a924907e5ac"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":

    # store the value of "main"
    # key in variable y
    y = x["main"]

    # store the value corresponding
    # to the "temp" key of y
    current_temperature = y["temp"]

    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding
    # to the "humidity" key of y
    current_humidity = y["humidity"]

    # store the value of "weather"
    # key in variable z
    z = x["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description = z[0]["description"]

    # print following values
    print(" Temperature (in kelvin unit) = " +
          str(current_temperature) +
          "\n atmospheric pressure (in hPa unit) = " +
          str(current_pressure) +
          "\n humidity (in percentage) = " +
          str(current_humidity) +
          "\n description = " +
          str(weather_description))

else:
    print(" City Not Found ")
'''
def K_to_F(K):
    return (K - 273.15) * 9/5 + 32

current = response = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=e91b4794a9aac2f29d302a924907e5ac&q=Gainesville").json()
Forecast =requests.get("http://api.openweathermap.org/data/2.5/forecast?lat=29.6520&lon=-82.3250&appid=e91b4794a9aac2f29d302a924907e5ac").json()
info = {}
info["currtemp"] = round(K_to_F(current["main"]["temp"]))
info["currkind"] = current["weather"][0]["description"]
info["currhumidity"] = current["main"]["humidity"]
info["high"] = round(K_to_F(current["main"]["temp_max"]))
info["low"] = round(K_to_F(current["main"]["temp_min"]))
print(Forecast["list"][0])