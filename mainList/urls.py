from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('finished', finished, name='finished'),
    path('post/<int:event_id>/', show_event, name='event'),
    path('post/registrations_<int:event_id>/', registrationForm, name='registrations'),
]