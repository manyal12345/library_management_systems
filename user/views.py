from rest_framework import viewsets
from django.contrib.auth.models import Group
from .models import CustomUser
from .serializers import CustomUserSerializer, GroupSerializer, CustomLoginSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CustomLoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email }, status=status.HTTP_200_OK)

    def delete(self, request):
        request.auth.delete()
        return Response(status=HTTP_200_OK)