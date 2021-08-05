from django.shortcuts import render

# folders

from .models import User
from .serializers import UserSerializerAccount, UserSerializerLogin

# django contrib

from django.contrib.auth import authenticate

# rest_framework

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# o que há de novo. CreateAPIView sendo utilizado para criar parte de login
class AccountsView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerAccount


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializerLogin(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=request.data['username'], password=request.data['password']
        )

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token":token.key}, status=status.HTTP_200_OK)


        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)




