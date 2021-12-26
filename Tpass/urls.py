"""Tpass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, login_view, logout_view

urlpatterns = [
    path('', home_view, name='primary_home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('nodin/',include('Nodin.urls',namespace='Nodin')),
    path('rnc/',include('RNC.urls',namespace='RNC')),
    path('tpass/',include('Nodin_to_Tpass.urls',namespace='Nodin_to_Tpass')),
    path('meas/',include('Meas.urls',namespace='Meas')),
    path('site_profile/',include('Site_Profile.urls',namespace='Site_Profile')),
    path('nocurr/',include('Network_Overview_Current.urls',namespace='Network_Overview_Current')),
    path('summary_all_program/',include('Summary_All_Program.urls',namespace='Summary_All_Program')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT )