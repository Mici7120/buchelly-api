from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from appuser.models import AppUser
from userrole.models import UserRole
from rest_framework.authtoken.models import Token

class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        pw = request.data.get('password')
    
        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response({"error":"User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if check_password(pw, user.password):
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token":token,
                "message":"Logins successful",
                "user_id":user.appuserid,
                "full_name":user.fullname,
                "email":user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class SignUp(APIView):
    def post(self, request):
        try:
            user = AppUser.objects.create(
                fullname = request.data.get("fullname"),
                username = request.data.get("username"),
                email = request.data.get("email"),
                password = request.data.get("password"),
            )
            return Response({}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":"Sign Up error"}, status=status.HTTP_400_BAD_REQUEST)
