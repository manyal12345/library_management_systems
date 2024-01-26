from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library.views import AuthorViewSet, BookViewSet, StaffViewSet, StudentViewSet
from .views import TransactionPDFView


router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'student', StudentViewSet, basename='student')
router.register(r'staff', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
    path('pdf/transaction-report/', TransactionPDFView.as_view(), name='transaction_pdf_report'),
]