from django.db import models
from user.models import CustomUser

# Create your models here.
# code for author class
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name

# code for book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(null=True)
    isbn = models.PositiveIntegerField(unique=True, null=True)
    category = models.CharField(max_length=50,default="Fiction")
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

# code for transaction model for library
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('BORROW', 'Borrow'), ('RETURN', 'Return'), ('RESERVE', 'Reserve')])
    transaction_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.transaction_type}"


