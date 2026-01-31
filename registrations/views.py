from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Registration
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_registrations(request):
    try:
        registrations=Registration.objects.filter(user=request.user)
        serializer=RegistrationSerializer(registrations,many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in(request):
    try:
        registration_code=request.data.get('registration_code')

        if not registration_code:
            return Response({'error':'Registration code is required'},status=status.HTTP_400_BAD_REQUEST)
        
        registration=Registration.objects.get(registration_code=registration_code)

        if registration.checked_in:
            return Response({'message':'Already checked in','checked_in_at':registration.checked_in_at},status=status.HTTP_200_OK)
        
        registration.checked_in=True
        registration.checked_in_at=timezone.now()
        registration.save()

        return Response({'message':'Check-in successful','event':registration.event.title,'user':registration.user.full_name},status=status.HTTP_200_OK)

    except Registration.DoesNotExist:
        return Response({'error':'Invalid registration code'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)