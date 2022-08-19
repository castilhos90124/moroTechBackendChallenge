import json

import requests
from book_rating_backend.commons.messages import Message
from rest_framework import status
from rest_framework.exceptions import APIException
from book_rating_backend.models import Book, BookReview
from django.core.exceptions import ObjectDoesNotExist


class BookService:

    def __init__(self):
        self.BOOK_API_URL = 'https://gutendex.com/books/'

    def get_books_by_title(self, book_title):
        query_param = F'?search={book_title}'
        return self.__get_book_data(query_param)['results']

    def get_book_details(self, book_id):
        book_details = self.__get_book_data(book_id)
        book_details['rating'] = self.__get_book_average_rating(book_id)
        book_details['reviews'] = self.__get_book_reviews(book_id)
        return book_details

    def __get_book_data(self, query_param=''):
        try:
            response = requests.get(F'{self.BOOK_API_URL}{query_param}')
            if response.status_code != status.HTTP_200_OK:
                raise APIException(Message.gutendex_error())
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    @staticmethod
    def __get_book_average_rating(book_id):
        try:
            book = Book.objects.get(id=book_id)
        except ObjectDoesNotExist:
            return None
        return round(float(book.rating_sum) / book.rating_count, 1)

    @staticmethod
    def __get_book_reviews(book_id):
        book_reviews_queryset = BookReview.objects.filter(book_id=book_id).values_list('review', flat=True)
        return list(book_reviews_queryset)

    @staticmethod
    def update_book_rating(book_id, rating):
        book, _ = Book.objects.get_or_create(
            id=book_id, defaults={'rating_sum': 0, 'rating_count': 0}
        )
        book.rating_sum += rating
        book.rating_count += 1
        book.save()
