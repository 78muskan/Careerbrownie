from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.mail import send_mail
from django.conf import settings
import requests as http_requests

from .models import User, EmailVerificationToken, PasswordResetToken
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, GoogleAuthSerializer,
)
from notifications.models import AuditLog


def _tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role
    refresh["full_name"] = user.full_name
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def _audit(request, user, action, description=""):
    AuditLog.objects.create(
        user=user, action=action, description=description,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )


def _send_verification_email(user, request):
    token = EmailVerificationToken.objects.create(
        user=user, expires_at=timezone.now() + timedelta(hours=24)
    )
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token.token}"
    send_mail(
        subject="Verify your MargVedA email",
        message=f"Hi {user.full_name},\n\nVerify your email:\n{verify_url}\n\nExpires in 24 hours.\n\n— MargVedA",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        if user.role == "student":
            from students.models import StudentProfile, CareerProfile
            profile = StudentProfile.objects.create(user=user)
            CareerProfile.objects.create(student=profile)
        _send_verification_email(user, request)
        _audit(request, user, "register", f"Registered as {user.role}")
        return Response({
            "message": "Account created! Check your email to verify.",
            "user": UserSerializer(user, context={"request": request}).data,
            **_tokens_for_user(user),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data["user"]
        user.update_last_login()
        _audit(request, user, "login")
        return Response({
            "user": UserSerializer(user, context={"request": request}).data,
            **_tokens_for_user(user),
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                RefreshToken(refresh_token).blacklist()
        except TokenError:
            pass
        _audit(request, request.user, "logout")
        return Response({"message": "Logged out successfully."})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user, context={"request": request}).data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            _audit(request, request.user, "profile_update")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token_val = request.data.get("token")
        if not token_val:
            return Response({"error": "Token required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = EmailVerificationToken.objects.get(token=token_val, is_used=False)
        except EmailVerificationToken.DoesNotExist:
            return Response({"error": "Invalid or used token."}, status=status.HTTP_400_BAD_REQUEST)
        if token.is_expired():
            return Response({"error": "Link expired. Request a new verification email."}, status=status.HTTP_400_BAD_REQUEST)
        token.user.is_verified = True
        token.user.save(update_fields=["is_verified"])
        token.is_used = True
        token.save(update_fields=["is_used"])
        return Response({"message": "Email verified!"})


class ResendVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_verified:
            return Response({"message": "Already verified."})
        _send_verification_email(request.user, request)
        return Response({"message": "Verification email sent."})


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower()
        try:
            user = User.objects.get(email=email)
            token = PasswordResetToken.objects.create(
                user=user, expires_at=timezone.now() + timedelta(hours=2)
            )
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token.token}"
            send_mail(
                subject="Reset your MargVedA password",
                message=f"Hi {user.full_name},\n\nReset your password:\n{reset_url}\n\nExpires in 2 hours.\n\n— MargVedA",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass
        return Response({"message": "If that email exists, a reset link has been sent."})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token_obj = serializer.validated_data["token_obj"]
        user = token_obj.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        token_obj.is_used = True
        token_obj.save(update_fields=["is_used"])
        _audit(request, user, "password_reset")
        return Response({"message": "Password reset. Please log in."})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"message": "Password changed."})


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data["access_token"]
        try:
            resp = http_requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )
            resp.raise_for_status()
            gdata = resp.json()
        except Exception:
            return Response({"error": "Failed to verify Google token."}, status=status.HTTP_400_BAD_REQUEST)

        email = gdata.get("email", "").lower()
        if not email:
            return Response({"error": "Google account has no email."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": gdata.get("name", email.split("@")[0]),
                "google_id": gdata.get("sub", ""),
                "auth_provider": "google",
                "is_verified": True,
                "role": "student",
            },
        )
        if not created and not user.google_id:
            user.google_id = gdata.get("sub", "")
            user.is_verified = True
            user.save(update_fields=["google_id", "is_verified"])

        if created and user.role == "student":
            from students.models import StudentProfile, CareerProfile
            profile = StudentProfile.objects.create(user=user)
            CareerProfile.objects.create(student=profile)

        user.update_last_login()
        _audit(request, user, "login", "Google OAuth")
        return Response({
            "user": UserSerializer(user, context={"request": request}).data,
            "is_new_user": created,
            **_tokens_for_user(user),
        })
