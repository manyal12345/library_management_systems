from rest_framework import serializers
from django.contrib.auth.models import Group
from user.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class CustomUserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'groups', 'is_staff', 'is_superuser', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        validated_data['password'] = make_password(validated_data.get('password'))
        user = CustomUser.objects.create(**validated_data)
        for group_data in groups_data:
            user.groups.add(group_data)
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data