from django.db import models


class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=20, unique=True)
    lat = models.FloatField(default=27.7172)
    lng = models.FloatField(default=85.3240)
    speed = models.FloatField(default=0)
    heading = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['vehicle_id']

    def __str__(self):
        return f"{self.vehicle_id} ({self.speed:.0f} km/h)"


class Accident(models.Model):
    SEVERITY_CHOICES = [
        ('Minor', 'Minor'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
        ('Fatal', 'Fatal'),
    ]

    vehicle = models.CharField(max_length=20)
    lat = models.FloatField()
    lng = models.FloatField()
    road_name = models.CharField(max_length=100, default="Unknown Road")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="Minor")
    description = models.TextField(default="Vehicle accident reported")
    injuries = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f"{self.vehicle} - {self.severity} @ {self.road_name}"


class Violation(models.Model):
    VIOLATION_TYPES = [
        ('Overspeeding', 'Overspeeding'),
        ('Wrong Lane', 'Wrong Lane'),
        ('Red Light', 'Red Light'),
        ('No Helmet', 'No Helmet'),
    ]

    vehicle = models.CharField(max_length=20)
    lat = models.FloatField()
    lng = models.FloatField()
    speed = models.FloatField()
    lane = models.CharField(max_length=10)
    violation_type = models.CharField(max_length=50, choices=VIOLATION_TYPES)
    video_clip = models.CharField(max_length=100)
    fine_amount = models.IntegerField(default=500)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f"{self.vehicle} - {self.violation_type} ({self.speed:.0f} km/h)"


class TrafficSignal(models.Model):
    SIGNAL_STATES = [
        ('Red', 'Red'),
        ('Yellow', 'Yellow'),
        ('Green', 'Green'),
    ]

    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    state = models.CharField(max_length=10, choices=SIGNAL_STATES, default='Green')
    cycle_time = models.IntegerField(default=60)

    def __str__(self):
        return f"{self.name} - {self.state}"
