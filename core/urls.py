from django.urls import path

from .views import CustomLogout, index, event_registration, booking_success, events, client_registration, company_registration, CustomLoginView, category, profile, company_home, company_event_list, create_event, company_profile

urlpatterns = [
    path('', index, name='home'),
    path('company/<int:company_id>/events/', events, name='events'),
    path('category/<int:category_id>/register/', category, name="category"),
    path('event/<int:event_id>/register/', event_registration, name='event_registration'),
    path('booking/<int:booking_id>/success/', booking_success, name='booking_success'),
    path('client-registration/', client_registration, name="client_registration"),
    path('company-registration/', company_registration, name="company_registration"),
    path('company-home', company_home, name="company_home"),
    path("company-event/<int:pk>/", company_event_list, name="company_event_list"),
    path('company-profile/',company_profile, name="company_profile"),
    path('create-event/', create_event, name="create_event"),
    path('profile/', profile, name="profile"),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogout, name='logout')    
    
]