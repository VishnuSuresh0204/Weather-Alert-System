from django.db import models
from django.contrib.auth.models import AbstractUser


class Login(AbstractUser):
    userType = models.CharField(max_length=50)
    # admin / fisher / rescue

    viewPass = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

class Port(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Fisherman(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    boat_number = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class RescueTeam(models.Model):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    port = models.ForeignKey(Port, on_delete=models.SET_NULL, null=True)
    profile_pic = models.ImageField(upload_to="rescue_profiles", null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return self.name


class WeatherAlert(models.Model):

    ALERT_LEVELS = (
        ('safe', 'Safe'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    port = models.ForeignKey(Port, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    alert_level = models.CharField(max_length=20, choices=ALERT_LEVELS)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_by = models.ForeignKey(Login, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class SOS(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('dispatched', 'Team Dispatched'),
        ('rescued', 'Rescued'),
        ('closed', 'Closed'),
    )

    fisherman = models.ForeignKey(Fisherman, on_delete=models.CASCADE)
    emergency_type = models.CharField(max_length=100)
    location_details = models.CharField(max_length=300)
    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS {self.id} - {self.fisherman.name}"


class RescueAction(models.Model):
    sos = models.ForeignKey(SOS, on_delete=models.CASCADE)
    rescue_team = models.ForeignKey(RescueTeam, on_delete=models.CASCADE)

    action_note = models.TextField()
    action_image = models.ImageField(
        upload_to="rescue_actions",
        null=True,
        blank=True
    )

    status_updated_to = models.CharField(
        max_length=20,
        choices=SOS.STATUS_CHOICES
    )

    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action on SOS {self.sos.id}"


class Notification(models.Model):
    fisherman = models.ForeignKey(Fisherman, on_delete=models.CASCADE)
    sos = models.ForeignKey(SOS, on_delete=models.CASCADE)

    message = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Feedback(models.Model):
    fisherman = models.ForeignKey(Fisherman, on_delete=models.CASCADE)
    sos = models.ForeignKey(SOS, on_delete=models.CASCADE)

    message = models.TextField()
    rating = models.IntegerField(null=True, blank=True)

    reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for SOS {self.sos.id}"
