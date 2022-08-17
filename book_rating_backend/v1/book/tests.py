from rest_framework import status
from rest_framework.reverse import reverse
from book_rating_backend.v1.commons.messages import Message
from book_rating_backend.v1.commons.tests import CustomAPITestCase


class BookTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()

        self.BASE_GET_URL = reverse('books-list')
        self.BOOK_ATTRIBUTES = set(
            ['id', 'title', 'authors', 'languages', 'download_count']
        )

    def test_get_books(self):
        query_param = 'book_title=Frankenstein'
        url = f'{self.BASE_GET_URL}?{query_param}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertExpectedFields(self.BOOK_ATTRIBUTES, response.data['books'][0])

    def test_get_books_without_query_param(self):
        response = self.client.get(self.BASE_GET_URL)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], Message.book_title_not_informed())
