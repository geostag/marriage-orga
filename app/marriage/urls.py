"""marriage URL Configuration

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
from django.urls import path
from django.conf.urls import include, url
import frontend.views

#handler403 = "v2.views.status403"
#handler404 = "v2.views.status404"
#if not settings.DEBUG:
#    handler500 = "v2.views.status500"


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', frontend.views.landingpage, name='landingpage'),
    path(r'frontend/',  include("frontend.urls")),
]
