from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework import status
from .serializers import UserSerializer,LoginSerializer,RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({
            "status": True,
            "data": serializer.data
        })
    



class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # ضمان أن الكائن المستخدم هو من نوع User المرتبط بـ Token
            user = User.objects.get(pk=user.pk)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "status": True,
                "message": "Logged in successfully",
                "token": token.key
            })
        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

    
class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": True,
                "message": "User registered successfully",
                "data": {
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # حذف التوكن الخاص بالمستخدم
        request.user.auth_token.delete()
        return Response({
            "status": True,
            "message": "Logged out successfully",
        })