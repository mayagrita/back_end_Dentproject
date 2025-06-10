from rest_framework import serializers
from .models import User  
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' # يمكنك تعديل الحقول كما تريد




class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(" The passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])  # تشفير الكلمة
        user.save()
        return user




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError("البريد الإلكتروني أو كلمة المرور غير صحيحة")

        if not check_password(password, user.password):
            raise serializers.ValidationError("البريد الإلكتروني أو كلمة المرور غير صحيحة")

        data['user'] = user
        return data