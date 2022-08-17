from book_rating_backend.v1.book.serializers import BookSerializer
from book_rating_backend.v1.book.services import BookService
from book_rating_backend.v1.commons.messages import Message
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response


class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        service = BookService()
        try:
            data = service.list_books_by_title(request.query_params['book_title'])
        except MultiValueDictKeyError:
            raise ParseError(Message.book_title_not_informed())

        serializer = BookSerializer(data, many=True)

        return Response({"books": serializer.data})
