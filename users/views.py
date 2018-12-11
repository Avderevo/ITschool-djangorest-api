#from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken

from rest_framework import viewsets
from users.models import Profile

from users import serializers


class ListUsers(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(APIView):

    permission_classes = (permissions.AllowAny,)


    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUser(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @api_view(['GET'])
# def current_user(request):
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data)


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializerWithToken(request.user)
        return Response(serializer.data)








class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    qs = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


'''
@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email).first()
        if user and User.check_password(user, password):
            try:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


class UserRetrieveUpdateAPIView():
    # Allow only authenticated users to access this url
    permission_classes = ()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK) 
'''