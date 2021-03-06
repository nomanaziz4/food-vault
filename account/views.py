from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import RegistrationSerializer, AccountPropertiesSerializer
from .models import Account
from rest_framework.authtoken.models import Token


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) != None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)

        username = request.data.get('username', '0')
        if validate_username(username) != None:
            data['error_message'] = 'That username is already in use.'
            data['response'] = 'Error'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            data['pk'] = account.pk
            print(account.pk)
            token = Token.objects.get(user=account).key
            data['token'] = token
            #data['mod'] = account.is_moderator
            if(account.is_moderator):
                data['mod'] = "true"
            else:
                data['mod'] = "false"
        else:
            data = serializer.errors
        return Response(data)


def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email, password)

        account = authenticate(email=email, password=password)

        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['token'] = token.key
            context['username'] = account.username
            if(account.is_moderator):
                context['mod'] = "true"
            else:
                context['mod'] = "false"
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'

        return Response(context)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ProfileInfo(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    lookup_field = "pk"
    serializer_class = AccountPropertiesSerializer

    def update(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
