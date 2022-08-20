from book_rating_backend.book import swagger_schema
from book_rating_backend.book.serializers import (BookDetailSerializer,
                                                  BookReviewSerializer,
                                                  BookSerializer)
from book_rating_backend.book.services import BookService
from book_rating_backend.commons.messages import Message
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response


@method_decorator(**swagger_schema.LIST)
@method_decorator(**swagger_schema.RETRIEVE)
class BookViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BookReviewSerializer

    def __init__(self, **kwargs: dict):
        self.service = BookService()

    def list(self, request: Request) -> Response:
        try:
            data = self.service.get_books_by_title(request.query_params['book_title'])
        except MultiValueDictKeyError:
            raise ParseError(Message.book_title_not_informed())

        serializer = BookSerializer(data, many=True)

        return Response({'books': serializer.data})

    def perform_create(self, serializer: BookReviewSerializer):
        with transaction.atomic():
            BookService.update_book_rating(self.request.data['book_id'], self.request.data['rating'])
            serializer.save()

    def retrieve(self, request: Request, **kwargs: dict) -> Response:
        data = self.service.get_book_details(kwargs.get('pk'))
        serializer = BookDetailSerializer(data)

        return Response(serializer.data)
