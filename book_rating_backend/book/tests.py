from rest_framework import status
from rest_framework.reverse import reverse
from book_rating_backend.commons.messages import Message
from rest_framework.test import APITestCase
from book_rating_backend.models import Book, BookReview



class BookTest(APITestCase):
    def setUp(self):
        super().setUp()

        self.BASE_URL = reverse('books-list')
        self.BOOK_ATTRIBUTES = set(
            ['id', 'title', 'authors', 'languages', 'download_count']
        )
        self.REVIEW_ATTRIBUTES = set(['uuid', 'book_id', 'rating', 'review'])
        self.DEFAULT_BODY_PARAMS = {
            'book_id': 1,
            'rating': 4,
            'review': 'An interesting book.'
        }

    def test_get_books(self):
        query_param = 'book_title=Frankenstein'
        url = f'{self.BASE_URL}?{query_param}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.BOOK_ATTRIBUTES, set(response.data['books'][0]))

    def test_get_books_without_query_param(self):
        response = self.client.get(self.BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], Message.book_title_not_informed())

    def test_post_book_review(self):

        response = self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.REVIEW_ATTRIBUTES, set(response.data))

        self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)
        book = Book.objects.get(id=self.DEFAULT_BODY_PARAMS['book_id'])

        self.assertEqual(book.id, self.DEFAULT_BODY_PARAMS['book_id'])
        self.assertEqual(book.rating_sum, self.DEFAULT_BODY_PARAMS['rating'] * 2)
        self.assertEqual(book.rating_count, 2)

    def test_post_book_review_with_wrong_rating(self):
        self.DEFAULT_BODY_PARAMS.update({'rating': 6})
        response = self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_book_review_without_review(self):
        del self.DEFAULT_BODY_PARAMS['review']

        response = self.client.post(self.BASE_URL, self.DEFAULT_BODY_PARAMS)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
