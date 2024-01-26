from datetime import timezone, datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from library.models import Author, Book, Transaction
from library.serializers import AuthorSerializer, BookSerializer, TransactionSerializer
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from django.http import HttpResponse
from django.views import View
from reportlab.pdfgen import canvas
from user.models import CustomUser

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author__name']


class StudentViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['user', 'book', 'transaction_type']

    def get_queryset(self):
        # Filter transactions based on the logged-in student
        return Transaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def borrowed_books(self, request):
        # Get a list of books borrowed by the student
        transactions = self.get_queryset().filter(transaction_type='BORROW')
        books = [transaction.book for transaction in transactions]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class StaffViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['user', 'book', 'transaction_type']

    def get_queryset(self):
        # Filter transactions based on the logged-in staff
        return Transaction.objects.all()

    @action(detail=False, methods=['get'])
    def overdue_books(self, request):
        # Get a list of overdue books
        current_time = datetime.now(timezone.utc)  # Use timezone.utc for UTC time
        overdue_transactions = self.get_queryset().filter(transaction_type='BORROW', due_date__lt=current_time)
        books = [transaction.book for transaction in overdue_transactions]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class TransactionPDFView(View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all()

        # Creating PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transaction_report.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, "Transaction Report")
        y_position = 780
        for transaction in transactions:
            p.drawString(100, y_position, f"Book: {transaction.book.title}")
            p.drawString(200, y_position, f"User: {transaction.user.username}")
            p.drawString(300, y_position, f"Transaction Type: {transaction.transaction_type}")
            y_position -= 20

        p.showPage()
        p.save()

        return response