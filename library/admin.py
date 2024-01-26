from django.contrib import admin

from library.models import Author, Book, Transaction

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Transaction)