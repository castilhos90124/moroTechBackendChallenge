from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from book_rating_backend.book.views import BookViewSet

schema_view = get_schema_view(
   openapi.Info(
      title='Books API',
      default_version='v1',
      description='MoroTech Backend Challenge',
   ),
   public=True,
)

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
