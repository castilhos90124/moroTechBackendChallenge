from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from book_rating_backend.v1.user import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
