# -*- coding: utf-8 -*-

import json
from apps.music.models import UsertoChart
from apps.music.models import Chart
from rest_framework import permissions, viewsets, status, views
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout

from apps.api.serializers import UserSerializer
from apps.users.models import User
from apps.users.permissions import IsAccountOwner


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        if self.request.method == 'POST':
            return permissions.AllowAny(),

        return permissions.IsAuthenticated(), IsAccountOwner(),

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            u2c = UsertoChart()
            try:
                chart = Chart.objects.get(name='Sylwester 2015/2016')
            except Chart.DoesNotExist:
                Chart.objects.create(name='Sylwester 2015/2016', owned_by=User.objects.get(username='automat'),
                votes_per_day=50, tracks_to_play=500)
            u2c.user = user
            u2c.chart = chart
            u2c.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'

        }, status=status.HTTP_400_BAD_REQUEST)


# views.APIView - are made specifically to handle AJAX requests.
class LoginView(views.APIView):
    # Logging is typically a POST request -> override the self.post() method.
    def post(self, request, format=None):
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)
        # authenticate checks if username exists in DB and given password is correct
        # returns User or None
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                # create a new session for this user.
                login(request, user)
                # We want to store some information about this user in the browser, so we serialize the User object
                # and return the resulting JSON as the response.
                serialized = UserSerializer(user)
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.',
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    # If you user is not authenticated, they will get a 403 error.
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

