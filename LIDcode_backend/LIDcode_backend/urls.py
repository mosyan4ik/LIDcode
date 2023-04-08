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

from coreApp.views import ParticipantAPIView, EventAPIView, TeamAPIView, MaterialAPIView, OrganizerAPIView, \
    SponsorAPIView


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/participant/', ParticipantAPIView.as_view()),
    path('api/v1/event/', EventAPIView.as_view()),
    path('api/v1/team/', TeamAPIView.as_view()),
    path('api/v1/material/', MaterialAPIView.as_view()),
    path('api/v1/organizer/', OrganizerAPIView.as_view()),
    path('api/v1/sponsor/', SponsorAPIView.as_view()),
]