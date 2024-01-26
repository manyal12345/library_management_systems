from rest_framework import serializers
from library.models import Author, Book, Transaction



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


# book serializer for the library to view create update and delete books
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'quantity_available']

    def validate_isbn(self, value):
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("ISBN must be unique.")
        return value

    def validate_quantity_available(self, value):
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Quantity available must be a positive integer.")
        return value

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author_instance = Author.objects.create(**author_data)
        book_instance = Book.objects.create(author=author_instance, **validated_data)
        return book_instance
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        instance.author.name = author_data.get('name', instance.author.name)
        instance.title = validated_data.get('title', instance.title)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.category = validated_data.get('category', instance.category)
        instance.quantity_available = validated_data.get('quantity_available', instance.quantity_available)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.save()
        return instance

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

