from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Cities"
        
    def __str__(self):
        return self.name

class WeatherRecord(models.Model):
    SOURCE_CHOICES = [
        ('api', 'API Fetch'),
        ('csv', 'CSV Import'),
    ]
    
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_records')
    date = models.DateField()
    temp_max = models.FloatField(null=True, blank=True)
    temp_min = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    wind_speed_max = models.FloatField(null=True, blank=True)
    precip_prob_max = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='api')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['city', 'date']
        
    def __str__(self):
        return f"{self.city.name} - {self.date}"

class CrimeIncident(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='crime_incidents')
    date_time = models.DateTimeField()
    reason = models.CharField(max_length=200)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_time']
        
    def __str__(self):
        return f"{self.reason} at {self.location or 'Unknown'} on {self.date_time}"
