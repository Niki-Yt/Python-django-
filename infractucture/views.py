from django.shortcuts import redirect, render, get_object_or_404
"""from django.http import HttpResponse"""
from .models import Weather
from django.contrib.auth.decorators import login_required
import csv
from django import forms
from .forms import CSVUploadForm, WeatherForm

def weather_list(request):
    weathers = Weather.objects.all()
    return render(request, 'weather_list.html', {'weathers': weathers})

"""@login_required
def secure_page(request):
    return render(request, 'secure.html')"""

"""def index(request):
    return HttpResponse("Test")"""
# Create your views here.

@login_required
def secure_page(request):
    return render(request, 'secure.html')

@login_required
def upload_csv_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                Weather.objects.create(
                    location=row['location'],
                    date=row['date'],
                    time=row['time'],
                    temp=row['temp'],
                    name=row['name'],
                    model=row['model'],
                    model_id=row['model_id'],
                )
            return redirect('upload-csv-success')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})

@login_required
def upload_csv_success_view(request):
    return render(request, 'upload_csv_success.html')


def sensor_list(request):
    sensors = Weather.objects.all()
    return render(request, 'weather_list.html', {'sensors': sensors})

def sensor_detail(request, sensor_id):
    sensor = get_object_or_404(Weather, id=sensor_id)
    return render(request, 'weather_detail.html', {'sensor': sensor})

def add_sensor(request):
    if request.method == 'POST':
        form = Weather(request.POST)
        if form.is_valid():
            form.save()
            return redirect('weather_list')
    else:
        form = Weather()
    return render(request, 'add_sensor.html', {'form': form})