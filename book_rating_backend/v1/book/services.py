import json

import requests
from book_rating_backend.v1.commons.messages import Message
from rest_framework import status
from rest_framework.exceptions import APIException

BOOK_API_URL = 'https://gutendex.com/books/'


class BookService:

    def list_books_by_title(self, book_title):
        return self.__get_book_data(book_title)

    @staticmethod
    def __get_book_data(book_title):
        try:
            response = requests.get(F'{BOOK_API_URL}?search={book_title}')
            if response.status_code != status.HTTP_200_OK:
                raise APIException(Message.gutendex_error())
            return json.loads(response.text)['results']
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
