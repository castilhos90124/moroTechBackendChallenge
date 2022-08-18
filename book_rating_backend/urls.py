from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from book_rating_backend.book.views import BookViewSet


router = routers.DefaultRouter()

router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
