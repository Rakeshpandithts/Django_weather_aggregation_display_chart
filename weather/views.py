from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from django.conf import settings
import os

value = settings.BASE_DIR

csvFilePath = os.path.join(settings.BASE_DIR, 'sensor_data.csv')
df = pd.read_csv(csvFilePath)


# Statistics function will give count, average, standard deviation, variance, sum, maximum, minimum 
def statistics(cleaned_data, column_nmae):
    count = cleaned_data[str(column_nmae)].count()
    average = cleaned_data[str(column_nmae)].mean().round(2)
    std_deviation = cleaned_data[str(column_nmae)].std().round(2)
    variance = cleaned_data[str(column_nmae)].var().round(2)
    sum = cleaned_data[str(column_nmae)].sum().round(2)
    maximum = cleaned_data[str(column_nmae)].max()
    minimum = cleaned_data[str(column_nmae)].min()
    stats = {
        'count': count,
        'average': average,
        'sum':sum,
        'maximum': maximum,
        'minimum': minimum,
        'std_deviation':std_deviation,
        'variance':variance
    }
    return stats
    
class HomeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'index.html')

class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format = None):
		timestamp = df.timestamp.tolist()
		chartLabel = "Data"
		chartdata = {
            'temperature' : [df.temp.tolist(), statistics(df, 'temp')],
            'pressure' : [df.pressure.tolist(), statistics(df, 'pressure')],
            'wind': [df.wind.tolist(), statistics(df, 'wind')],
            'humidity': [df.humidity.tolist(), statistics(df, 'humidity')]
        }
		data ={
					"labels":timestamp,
					"chartLabel":chartLabel,
					"chartdata":chartdata,
			}
		return Response(data)

def get_weather_stats(request):
    context = {
            'temperature' : statistics(df, 'temp'),
            'pressure' : statistics(df, 'pressure'),
            'wind': statistics(df, 'wind'),
            'humidity': statistics(df, 'humidity')
        }

    print(context)
    return render(request, 'weather.html', context)