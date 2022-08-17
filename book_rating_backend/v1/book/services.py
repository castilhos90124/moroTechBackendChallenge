import requests
import json
from rest_framework import status
from rest_framework.exceptions import APIException

BOOK_API_URL = "https://gutendex.com/books/"


class BookService:

    def list_books_by_title(self, book_title):
        return self.__get_book_data(book_title)

    @staticmethod
    def __get_book_data(book_title):
        try:
            response = requests.get(F'{BOOK_API_URL}?search={book_title}')
            if response.status_code != status.HTTP_200_OK:
                raise APIException("Error getting books information from Gutendex API")
            return json.loads(response.text)['results']
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)