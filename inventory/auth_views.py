from django.contrib.auth.models import User
from django.urls import path
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from .auth_serializers import EmailTokenObtainPairSerializer
from .models import RegistrationCode

class RequestEmailCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone_number')

        if not email or not phone:
            return Response({'error': 'Email and phone required'}, status=400)

        code = f"{random.randint(100000, 999999)}"

        RegistrationCode.objects.update_or_create(
            email=email,
            defaults={'phone_number': phone, 'code': code}
        )

        # Prepare and send styled HTML email
        subject = 'Your Registration Code'
        from_email = 'bonheurndezenc@gmail.com'
        to = [email]

        context = {'code': code, 'email': email}
        html_content = render_to_string('emails/registration_code.html', context)
        text_content = f"Hello,\n\nYour confirmation code is {code}.\n\nRegards,\nSeed Distribution Team"

        email_msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        return Response({'message': 'Code sent successfully'})

class ConfirmEmailCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({'error': 'Email and code are required'}, status=400)

        try:
            reg_code = RegistrationCode.objects.get(email=email, code=code)

            if reg_code.is_expired():
                return Response({'error': 'Code expired'}, status=400)

            reg_code.is_verified = True
            reg_code.save()
            return Response({'message': 'Email verified successfully'})
        
        except RegistrationCode.DoesNotExist:
            return Response({'error': 'Invalid code or email'}, status=400)


class SetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=400)

        try:
            reg = RegistrationCode.objects.get(email=email)

            if not reg.is_verified:
                return Response({'error': 'Email not verified'}, status=403)

            if User.objects.filter(email=email).exists():
                return Response({'error': 'User already exists'}, status=409)

            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()

            return Response({'message': 'Account created successfully'})
        
        except RegistrationCode.DoesNotExist:
            return Response({'error': 'Email not found'}, status=404)


class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

urlpatterns = [
    path('login/', EmailLoginView.as_view(), name='email_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-code/', RequestEmailCodeView.as_view(), name='request_email_code'),
    path('verify-code/', ConfirmEmailCodeView.as_view(), name='confirm_email_code'),
    path('set-password/', SetPasswordView.as_view(), name='set_password'),
]
