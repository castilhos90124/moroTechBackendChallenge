from book_rating_backend.book.serializers import BookSerializer, BookReviewSerializer, BookDetailSerializer
from django.db import transaction
from book_rating_backend.book.services import BookService
from book_rating_backend.commons.messages import Message
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookReviewSerializer

    def list(self, request):
        service = BookService()
        try:
            data = service.get_books_by_title(request.query_params['book_title'])
        except MultiValueDictKeyError:
            raise ParseError(Message.book_title_not_informed())

        serializer = BookSerializer(data, many=True)

        return Response({'books': serializer.data})

    def perform_create(self, serializer):
        with transaction.atomic():
            BookService.update_book_rating(self.request.data['book_id'], self.request.data['rating'])
            serializer.save()

    def retrieve(self, request, *args, **kwargs):
        service = BookService()
        data = service.get_book_details(kwargs.get('pk'))
        serializer = BookDetailSerializer(data)

        return Response(serializer.data)
