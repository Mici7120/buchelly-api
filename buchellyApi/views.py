from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from appuser.models import AppUser
from appuser.models import PasswordResetToken
from userrole.models import UserRole
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .utils import generate_token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework import serializers
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .utils import generate_jwt_token


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        pw = request.data.get("password")

        try:
            user = AppUser.objects.get(email=email)

            if check_password(pw, user.password):
                token = generate_jwt_token(user.email)

                return Response(
                    {
                        "token": token,
                        "message": "Login successful",
                        "full_name": user.fullname,
                        "email": user.email,
                        "id": user.id,
                        "role": user.userroleid.name,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )

        except AppUser.DoesNotExist:
            return Response(
                {"error": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print(e)
            return Response(
                {"error": "An error occurred during login", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Verificar si el rol "Client" existe; si no, crearlo
            client_role, created = UserRole.objects.get_or_create(
                name="Client", defaults={"status": True}
            )
    
            admin_role, created_admin = UserRole.objects.get_or_create(
                name="Admin", defaults={"status": True}
            )

            # si el rol como data es exactamente igual a "Admin" se asigna el rol de Admin, si no se asigna el rol de Client (tambien aplica si no se pasa el rol)
            role_name = admin_role if request.data.get("role") == "Admin" else client_role

            # Crear un nuevo usuario con el rol "Client"
            user = AppUser.objects.create(
                fullname=request.data.get("fullname"),
                email=request.data.get("email"),
                password=make_password(request.data.get("password")),
                userroleid=role_name,
            )

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(e)
            return Response(
                {"error": "Sign Up error"}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response(
                {"error": "No se encuentran registros asociados a ese correo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, expiration_date = generate_token(user.id)
        PasswordResetToken.objects.create(
            user=user, token=token, expiration_date=expiration_date
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/auth/change-password/{uid}/{token}/"

        try:
            send_mail(
                "Solicitud de restablecimiento de contraseña",
                f"Haz click en el link para cambiar tu contraseña: {reset_link}",
                "test@test.com",
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Error enviando el correo"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Correo de restablecimiento de contraseña enviado"},
            status=status.HTTP_200_OK,
        )


class PasswordResetTokenValidationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            appuserid = force_str(urlsafe_base64_decode(uidb64))
            user = AppUser.objects.get(id=appuserid)
        except (TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
            return Response(
                {"error": "Token o usuario inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            password_reset_token = PasswordResetToken.objects.get(
                user=user, token=token
            )
            if password_reset_token.is_expired():
                return Response(
                    {"error": "El token ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"error": "Token no válido"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "Token válido"}, status=status.HTTP_200_OK)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            appuserid = force_str(urlsafe_base64_decode(uidb64))
            user = AppUser.objects.get(id=appuserid)
        except (TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
            return Response(
                {"error": "Token o usuario inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            password_reset_token = PasswordResetToken.objects.get(
                user=user, token=token
            )
            if password_reset_token.is_expired():
                return Response(
                    {"error": "El token ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"error": "Token no válido"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user.password = make_password(serializer.validated_data["new_password"])
            user.save()

            PasswordResetToken.objects.filter(user=user, token=token).delete()
            return Response(
                {"message": "La contraseña ha sido cambiada"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
