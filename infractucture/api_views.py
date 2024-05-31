from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Weather
from .serializers import WeatherSerializer
import csv
import io

@api_view(['GET'])
def weather_list(request):
    weathers = Weather.objects.all()
    serializer = WeatherSerializer(weathers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def weather_detail(request, pk):
    try:
        weather = Weather.objects.get(pk=pk)
    except Weather.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = WeatherSerializer(weather)
    return Response(serializer.data)

@api_view(['GET'])
def weather_by_location(request, location):
    weathers = Weather.objects.filter(location=location)
    serializer = WeatherSerializer(weathers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def weather _create(request):
    serializer = WeatherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def upload_csv(request):
    file = request.FILES['file']
    if not file.name.endswith('.csv'):
        return Response({'error': 'Файо не відповідає CSV типу'}, status=status.HTTP_400_BAD_REQUEST)
    
    data_set = file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)  # пропустити заголовок
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Weather.objects.update_or_create(
            location=column[0],
            date=column[1],
            time=column[2],
            temp=column[3],
            name=column[4],
            model=column[5],
            model_id=column[6],
        )
    return Response({'status': 'CSV файл успішено завантажено!'}, status=status.HTTP_201_CREATED)