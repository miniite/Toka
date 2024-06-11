import random
from faker import Faker
from django.contrib.auth import get_user_model
from core.models import Client, Company, Event, Booking

User = get_user_model()

fake = Faker()

# Create 10 companies
for _ in range(10):
    email = fake.company_email()
    password = 'password'  # Set a default password
    country = fake.country()
    name = fake.company()
    phone = fake.phone_number()
    location = fake.address()
    company = Company.objects.create(email=email, password=password, country=country, name=name, phone=phone, location=location)

# Create 30 clients
for _ in range(30):
    email = fake.email()
    password = 'password'  # Set a default password
    country = fake.country()
    mobile = fake.phone_number()
    dob = fake.date_of_birth()
    Client.objects.create(email=email, password=password, country=country, mobile=mobile, dob=dob)

# Create 10 events for each company
companies = Company.objects.all()
for company in companies:
    for _ in range(10):
        name = fake.catch_phrase()
        date = fake.date_this_year()
        time = fake.time()
        location = fake.address()
        description = fake.paragraph()
        Event.objects.create(name=name, date=date, time=time, location=location, description=description, owner=company)

# Create random bookings
clients = Client.objects.all()
events = Event.objects.all()
for _ in range(100):
    client = random.choice(clients)
    event = random.choice(events)
    Booking.objects.create(client=client, event=event, approved=random.choice([True, False]))
