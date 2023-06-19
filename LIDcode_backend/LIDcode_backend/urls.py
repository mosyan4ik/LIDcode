"""LIDcode_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from coreApp.views import *


urlpatterns = [
    path('api/v1/participants/', ParticipantsAPIView.as_view()),
    path('api/v1/events/', EventsAPIView.as_view()),
    path('api/v1/teams/', TeamsAPIView.as_view()),
    path('api/v1/sponsors/', SponsorsAPIView.as_view()),
    path('api/v1/organizers/', OrganizersAPIView.as_view()),
    path('api/v1/materials/', MaterialsAPIView.as_view()),
    path('api/v1/users/', UsersAPIView.as_view()),
    path('api/v1/event_material/', EventMaterialAPIView.as_view()),
    path('api/v1/event_organizer/', EventOrganizerAPIView.as_view()),
    path('api/v1/event_sponsor/', EventSponsorAPIView.as_view()),

    path('api/v1/events_on_main_list/', EventsOnMainListAPIView.as_view()),
    path('api/v1/event_info_all/', EventInfoAllAPIView.as_view()),
    path('api/v1/event_info_regulations/', EventInfoRegulationsAPIView.as_view()),
    path('api/v1/event_check_registration/', EventCheckRegistrationAPIView.as_view()),
    path('api/v1/team_registration/', TeamRegistrationAPIView.as_view()),
    path('api/v1/user_login/', UserLoginAPIView.as_view()),
]






