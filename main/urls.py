from django.urls import path

from main import views

urlpatterns = [
    path("register", views.register),
    path("loginHtml", views.login_html),
]