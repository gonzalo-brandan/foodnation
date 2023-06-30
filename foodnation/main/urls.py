from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    #path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign_up"),
    path("create-post", views.create_post, name="create_post"),
    path("contact", views.contact, name="contact")

]