from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("item/", include("item.urls")),
    #path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign_up"),
    path("create-post", views.create_post, name="create_post"),
    path("contact", views.contact, name="contact")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)