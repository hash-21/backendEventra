from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from .serializers import SessionCreateUpdateSerializer, SessionSerializer
from .models import Session, Event
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_sessions(request,event_id):
    try:
        sessions=Session.objects.filter(event_id=event_id)

        track=request.query_params.get('track')
        if track:   
            sessions=sessions.filter(track=track)

        room=request.query_params.get('room')
        if room:   
            sessions=sessions.filter(room=room)

        serializer=SessionSerializer(sessions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session_detail(request,pk):
    try:
        session=Session.objects.get(pk=pk)
        serializer=SessionSerializer(session)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Session.DoesNotExist:
        return Response({'error':'Session not found'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_session(request):
    try:
        event_id=request.data.get('event')
        event=Event.objects.get(id=event_id)

        if event.organizer!=request.user:
            return Response({
                'error':'Only event organizer can create sessions'
            },status=status.HTTP_403_FORBIDDEN)
        
        serializer=SessionCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            session=serializer.save()
            response_data=SessionSerializer(session)
            return Response(response_data.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    except Event.DoesNotExist:
        return Response({'error':'Event not found'},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_session(request, pk):
    try:
        session=Session.objects.get(pk=pk)

        if session.event.organizer!=request.user:
            return Response({
                'error':'only event organizer can update sessions'
            },status=status.HTTP_403_FORBIDDEN)
        serializer=SessionCreateUpdateSerializer(session,data=request.data,partial=True)
        if serializer.is_valid():
            session=serializer.save()
            response_data=SessionSerializer(session)
            return Response(response_data.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    except Event.DoesNotExist:
        return Response({'error':'Event not found'},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_session(request, pk):
    try:
        session=Session.objects.get(pk=pk)

        if session.event.organizer!=request.user:
            return Response({
                'error':'only event organizer can delete sessions'
            },status=status.HTTP_403_FORBIDDEN)
        
        session.delete()
        return Response({'message':'Session deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    except Session.DoesNotExist:
        return Response({'error':'Session not found'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




