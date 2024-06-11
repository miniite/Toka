from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Add other fields like name, mobile, dob, etc.

    objects = CustomUserManager()
    username = None
    unique_together = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Client(CustomUser):
    name = models.CharField(max_length=255)    
    # Add other fields specific to the Client model
    
    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.email
    
class CompanyCategory(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields specific to the CompanyCategory model
    class Meta:
        verbose_name_plural = "Company Categories"


    def __str__(self):
        return self.name

class Company(CustomUser):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(CompanyCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.email


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Add other fields specific to t
    # he Event model
    class Meta:
        verbose_name_plural = "Events"
    
    def get_registration_count(self):
        return self.booking_set.count()

    def __str__(self):
        return self.name

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    queue_token = models.CharField(max_length=10, unique=True, blank=True)
    approved = models.BooleanField(default=False)
    # Add other fields specific to the Booking model 
    class Meta:
        verbose_name_plural = "Bookings"
        
    def save(self, *args, **kwargs):
        if not self.queue_token:
            self.queue_token = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.client.email + " - " + self.event.name