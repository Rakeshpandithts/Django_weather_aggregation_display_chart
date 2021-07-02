from json import dump
import random
import datetime
import logging
import time
import sys

# create log file every day based on date log file name is date.log
logFileName= datetime.datetime.now().strftime("%m_%d_%Y") + ".log"  #log file name cration
logging.basicConfig(filename=logFileName,  format='%(asctime)s %(message)s', level=logging.DEBUG) # creating logging configuration


# city dictionary contains city name, latitude and longitude data
city_dictionary = {
  "London" : (51.50, -0.12),  # city name longitude and lattitude Tuple
  "New York": (40.71, -74.00),
  "Bangalore": (12.97, 77.59)
}

def write_weather_data():
  while True:
    # get random city data from dictionary
    random_city_data = random.choice(list(city_dictionary.items())) # geting random city name, latitude and longitude from dictionary

    #prepare random weather data dictionary
    try:
      weather_data = {
        "name": str(random_city_data[0]),  # city name to dictionary as string
        "lat": random_city_data[1][0],      # latitude to dictionary as float
        "lon": random_city_data[1][1],      # longitude to dictionary as float
        "last_updated_epoch": datetime.datetime.now().timestamp(), # Generating current timestamp from datetime library
        "temp_f": round(random.uniform(49, 70), 2),  # Generating random temperature data in range 49 to 70 and decimal rounding off to 2 digits
        "wind_kph": round(random.uniform(0, 11), 2),  # Generating random wind data in range 0 to 11 and decimal rounding off to 2 digits
        "pressure_mb": random.randint(970,1025),      # Generating random wind data in range 970 to 1025
        "humidity": random.randint(60,85)             # Generating random wind data in range 60 to 85
      }
      logging.info('Weather data created')
    except:
      print('Error while creating random weatehr data')
      logging.error('Error while creating random weatehr data')
      sys.exit()


    # check the weather data lies in the required range, if it is in range write the weather  data to a text file else ignore the data.
    if 50<= weather_data['temp_f'] <=65 and 0<= weather_data['wind_kph'] <10 & 975 <= weather_data['pressure_mb'] <= 1020 and 60<=weather_data['humidity']<=80: #data anomaly checking
      print('correct weather_data')
      try:
        print(weather_data)
        with open('sensor_data.txt', 'a+') as file: # opening text file to append data
          dump(weather_data, file, ensure_ascii=False) # dumping weather data dictionary to text file
        file.close()                                    # closing the text file
        logging.info('writing sensor data')
      except:
        print('Error while writing the sensor data to text file')
        logging.error('Error while writing the sensor data to text')
    else:
      print('Weather data anomaly detected weather data =  {}'.format(weather_data))
      logging.error('Weather data anomaly detected weather data =  {}'.format(weather_data))
    
    time.sleep(5)       # Delay 5 seconds


if __name__ == "__main__":
  write_weather_data()