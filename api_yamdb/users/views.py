from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import  UserSerializer, EmailSerializer, ConfirmationCodeSerializer 
from .models import User
from .permission import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )

class EmailRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def mail_send(email, user):
        send_mail(
            subject=' Confirmation Code',
            message=f'Your confirmation: '
                    f'{user.confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        serializer.save(email=email)
        user = get_object_or_404(User, email=email)
        self.mail_send(email, user)
        return Response({f'email: {email}'}, status=status.HTTP_200_OK)


class AccessTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'email':
                    'Not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.confirmation_code != confirmation_code:
            return Response({
                'confirmation_code':
                    f'Invalid confirmation code for email {user.email}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.get_token(user), status=status.HTTP_200_OK)

    @staticmethod
    def get_token(user):
        return {
            'token': str(AccessToken.for_user(user))
        }
