from django.db import models

class Weather(models.Model):
    location = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    temp = models.IntegerField()
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    model_id = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.sensor_name} at {self.location} on {self.measurement_date} {self.measurement_time}"

# Create your models here.
