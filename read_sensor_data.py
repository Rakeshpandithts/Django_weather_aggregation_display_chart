from json import JSONDecoder, JSONDecodeError
import pandas as pd
import sys
import logging
import datetime

weather_data_list = []


# create log file every day based on date log file name is date.log
logFileName= datetime.datetime.now().strftime("%m_%d_%Y") + ".log" #log file name cration date wise every day
logging.basicConfig(filename=logFileName,  format='%(asctime)s %(message)s', level=logging.DEBUG) # creating logging configuration


#read text file  => This function opens a text file and decodes the JSON data then returns a pandas dataframe which contains all sensor data.
def read_sensor_data():
  try:
    with open('sensor_data.txt') as fi:  # opening text file to append data
      data = fi.read()                    # reading text file data
    decoder = JSONDecoder()               # calling json decoder
    pos = 0
    while True:
        try:
            o, pos = decoder.raw_decode(data, pos) # decoding the text file data as JSON 
            weather_data_list.append(o)             # appending data to weather data list creating list of JSON 
        except JSONDecodeError:
            break
    if len(weather_data_list) == 0:
      df = pd.DataFrame(columns =["name", "lat","lon", "last_updated_epoch", "temp_f", "wind_kph", "pressure_mb", "humidity"  ]) # creating pandas data frame with column name
      print('text file doesnt contain any data created a empty data frame')
      logging.info('text file doesnt contain any data created a empty data frame')
    else:      
      df = pd.DataFrame(weather_data_list) # creating pandas dataframe with list of weather data JSON
    return df
  except:
    print('error while reading the txt file')
    print('exiting program')
    logging.error('error while reading the txt file exiting program')

    sys.exit()

# clean and convert data sensor data
def clean_sensor_data(raw_data):
  # Give the variables some friendlier names and convert types and unit as necessary.
  df = pd.DataFrame()
  df['location'] = raw_data['name']                                                   # changing column name from name to location
  df['temp'] = raw_data['temp_f'].astype(float).apply(lambda x: (x-32)/1.8).round(2)  # converting fahrenheit to celsius and changing type to float and rounding float decimal to 2 digits
  df['wind'] = raw_data['wind_kph'].astype(float).round(2)                            #  changing type to float and rounding float decimal to 2 digits
  df['pressure'] = raw_data['pressure_mb']                                            # changing column name from pressure_mb to pressure
  df['humidity'] = raw_data['humidity']                                                           
  df['timestamp'] = raw_data['last_updated_epoch']                                      # changing column name from last_updated_epoch to timestamp

  return df

# Statistics function will give count, average, standard deviation, variance, sum, maximum, minimum 
def statistics(cleaned_data, column_nmae):
  count = cleaned_data[str(column_nmae)].count()                            #Getting indivitual data count
  average = cleaned_data[str(column_nmae)].mean().round(2)                  # averaging the individual data 
  std_deviation = cleaned_data[str(column_nmae)].std().round(2)             # calculating STANDARD DEVIATION of individual data
  variance = cleaned_data[str(column_nmae)].var().round(2)                  # calculating VARIANCE of individual data
  sum = cleaned_data[str(column_nmae)].sum().round(2)                       # calculating TOTAL SUM of individual data
  maximum = cleaned_data[str(column_nmae)].max()                            # getting maximum value in a individual data values
  minimum = cleaned_data[str(column_nmae)].min()                            # getting minimum value in a individual data values
  print(count, average, sum, maximum, minimum, std_deviation, variance)
  print('*************************************************************')
  print("***************{} STATISTICS*****************".format(column_nmae))
  print('*************************************************************')
  print('count = {}'.format(count))
  print('average = {}'.format(average))
  print('sum = {}'.format(sum))
  print('maximum = {}'.format(maximum))
  print('minimum = {}'.format(minimum))
  print('std_deviation = {}'.format(std_deviation))
  print('variance = {}'.format(variance))

raw_data = read_sensor_data()
print(raw_data)
if raw_data.empty:
    print('empty data')
    df = pd.DataFrame()
    df['location'] = raw_data['name']
    df['temp'] = raw_data['temp_f']
    df['wind'] = raw_data['wind_kph']
    df['pressure'] = raw_data['pressure_mb']
    df['humidity'] = raw_data['humidity']
    df['timestamp'] = raw_data['last_updated_epoch']
    df.to_csv('sensor_data.csv')
    sys.exit()
else:
  cleaned_data = clean_sensor_data(raw_data)
  cleaned_data.to_csv('sensor_data.csv')
  statistics(cleaned_data, 'temp')
  statistics(cleaned_data, 'pressure')
  statistics(cleaned_data, 'wind')
  statistics(cleaned_data, 'humidity')
