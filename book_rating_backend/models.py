from django.db import models
import uuid


class Book(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, editable=False)
    rating_sum = models.PositiveIntegerField()
    rating_count = models.PositiveIntegerField()
    created = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = "book"


class BookReview(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=1000)
    created = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = "book_review"
