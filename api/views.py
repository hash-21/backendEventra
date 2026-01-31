from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer, LoginSerializer, 
    UserSerializer, ProfileUpdateSerializer
)
from django.contrib.auth import authenticate, get_user_model

User=get_user_model()
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    try:
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
           user=serializer.save()

           refresh=RefreshToken.for_user(user)

           return Response({
               'message':'User registered successfully',
               'user':UserSerializer(user).data,
               'tokens':{
                   'refresh':str(refresh),
                   'access':str(refresh.access_token),
                   }

           },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return Response({
            'error':'User with this email or username already exists'

        },status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error':'Registration failed, please try again.',
            'detail':str(e),

        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        serializer=LoginSerializer(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']

            user=authenticate(request,username=email,password=password)

            if user is not None:
                refresh=RefreshToken.for_user(user)

                return Response({
                    'message':'Login successful',
                    'user':UserSerializer(user).data,
                    'tokens':{
                        'refresh':str(refresh),
                        'access':str(refresh.access_token)
                    }

                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':'Invalid username or password'
                },status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    except Exception as e:
        return Response({
            'error':'Login failed.Please try again.',
            'detail':str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    try:
        if request.method=='GET':
            serializer=UserSerializer(request.user)
            return Response(serializer.data)
        
        elif request.method=='PUT':
            serializer=ProfileUpdateSerializer(
                request.user,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message':'Profile updated successfully',
                    'user':UserSerializer(request.user).data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    except Exception as e:
        return Response({
            'error':'Profile operation failed.',
            'detail':str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token=request.data.get('refresh')
        if refresh_token:
            token=RefreshToken(refresh_token)
            token.blacklist()
        return Response({
            'message':'Logout successful'
        },status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error':'Logout failed',
            'detail':str(e)

        },status=status.HTTP_400_BAD_REQUEST)


