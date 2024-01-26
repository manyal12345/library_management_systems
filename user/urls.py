from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import CustomLoginView, CustomUserViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
]
