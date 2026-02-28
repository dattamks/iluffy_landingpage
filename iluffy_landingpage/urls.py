"""
URL configuration for iluffy_landingpage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve
from pathlib import Path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("sitemap.xml", serve, {"document_root": Path(__file__).resolve().parent.parent / "static", "path": "sitemap.xml"}, name="sitemap"),
    path("logo.png", serve, {"document_root": Path(__file__).resolve().parent.parent / "static" / "img", "path": "logo.png"}, name="logo"),
    path("", include("main.urls")),
]
