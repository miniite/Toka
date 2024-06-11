from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib import messages  # Import messages module for error messages
from .models import Event, Booking, Company, CompanyCategory
from .forms import ClientRegistrationForm, CompanyRegistrationForm



@login_required
def index(request):
    try:
        if request.user.company:
            return redirect("company_home")
    except:
        categories = CompanyCategory.objects.all()
        return render(request, 'index.html', {'categories': categories})


@login_required
def company_home(request):
    events = Event.objects.filter(owner=request.user.company)
    return render(request, 'company_home.html', {'events': events})

@login_required
def category(request, category_id):
    category = CompanyCategory.objects.filter(pk=category_id).first()
    companies = Company.objects.filter(category=category)
    return render(request, 'company_list.html', {'companies': companies})

@login_required
def events(request, company_id):
    company = Company.objects.get(pk=company_id)
    events = Event.objects.filter(owner=company)
    return render(request, 'events_list.html', {'events': events, 'company': company})

@login_required
def event_registration(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        booking = Booking.objects.create(
            client = request.user.client,
            event = event
        )
        return redirect('profile')
    return render(request, 'event_registration.html', {'event': event})

@login_required
def booking_success(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})


def client_registration(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        # breakpoint()
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')  # Replace 'home' with the appropriate URL
        else:
            # If the form is invalid, display error messages for each field
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = ClientRegistrationForm()
    return render(request, 'client_registration.html', {'form': form})


def company_registration(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('company_home')  # Replace 'home' with the appropriate URL
    else:
        form = CompanyRegistrationForm()
    return render(request, 'company_registration.html', {'form': form})



class CustomLoginView(View):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            # breakpoint()
            try:
                if user.client:
                    return redirect('home')  # Redirect on successful login
            except:
                if user.company:
                    return redirect("company_home")
        else:
            message = "Invalid credentials"
            messages.error(request, message)  # Display error message

        return render(request, self.template_name, {'message': message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
@login_required
def CustomLogout(request):
    logout(request)
    return HttpResponse("Loggged out")

@login_required
def profile(request):
    try:
        user = request.user.client
        booking = Booking.objects.filter(client=user)
        return render(request, 'profile.html', {'booking': booking })
    except:
        return redirect("company_profile")
@login_required
def company_profile(request):
    company = request.user.company
    return render(request, 'company-profile.html', {'company': company })

@login_required
def company_event_list(request, pk):
    company = request.user.company
    event = Event.objects.get(id=pk)
    booking = Booking.objects.filter(event__owner = company, event=event)
    # breakpoint()
    return render(request, 'company-event.html', {'bookings': booking})

@login_required
def create_event(request):
    if request.method == "POST":
        name = request.POST.get("name", '')
        date = request.POST.get("date", '')
        time = request.POST.get("time", '')
        location = request.POST.get("location", '') 
        description = request.POST.get('decription', '')

        owner = request.user.company

        Event.objects.get_or_create(name=name, date=date, time=time, location=location, description=description, owner=owner)

        return render(request, 'company_home.html')
    return render(request, 'create-event.html')