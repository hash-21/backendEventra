from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer,EventListSerializer,EventCreateUpdateSerializer
from .models import Event
from registrations.models import Registration
import qrcode
import requests
import re
import json
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile
from registrations.serializers import RegistrationSerializer
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_events(request):
    try:
        events=Event.objects.all()

        category=request.query_params.get('category')
        if category:
            events=events.filter(category=category)


        
        city=request.query_params.get('city')
        if city:
            events=events.filter(city__icontains=city)

        search=request.query_params.get('search')
        if search:
            events=events.filter(title__icontains=search)

        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_detail(request,pk):
    try:
        event=Event.objects.get(pk=pk)
        serializer=EventSerializer(event,context={'request':request})
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({'error':'Event not found'},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_events(request):
    try:
        events=Event.objects.filter(organizer=request.user)
        serializer=EventSerializer(events,many=True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request,pk):
    try:
        event=Event.objects.get(pk=pk)

        if event.organizer!=request.user:
             return Response({'error':'Only organizer can delete'},status=status.HTTP_403_FORBIDDEN)
        
        event.delete()
        return Response({'message': 'Event deleted'}, status=status.HTTP_204_NO_CONTENT)
        
    except Event.DoesNotExist:
        return Response({'error':'Event not found'},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        serializer=EventCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            event=serializer.save(organizer=request.user)
            response=EventSerializer(event,context={'request':request})
            return Response(response.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


      
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request,pk):
    try:
        event=Event.objects.get(pk=pk)

        if event.organizer!=request.user:
             return Response({'error':'Only organizer can update'},status=status.HTTP_403_FORBIDDEN)
        serializer=EventCreateUpdateSerializer(event,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response=EventSerializer(event,context={'request':request})
            return Response(response.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    except Event.DoesNotExist:
        return Response({'error':'Event not found'},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_event_recommendations(request):
    try:
        print("VIEW HIT")  # check if view is reached at all
        print("GEMINI KEY:", settings.GEMINI_API_KEY)
        print("GEMINI KEY:", settings.GEMINI_API_KEY) 

        user_interests=request.data.get('userInterests','').strip()
        available_events=request.data.get('availableEvents',[])
   

        if not user_interests:
            return Response({'error':'Please Enter your interests.'},status=status.HTTP_400_BAD_REQUEST)
        
        if not available_events:
            return Response({'error':'No events available.'},status=status.HTTP_400_BAD_REQUEST)

        events_text = '\n'.join([
            f"{idx + 1}. {event['title']}\n"
            f"Category: {event.get('category', 'General')}\n"
            f"Description: {event.get('description', 'No description available')}\n"
            f"Date: {event['date']}\n"
            f"Location: {event['location']}\n"
            for idx, event in enumerate(available_events)
        ])
        
        prompt = f"""You are an intelligent event recommendation system. Based on the user's interests, recommend the most relevant events from the list and explain why they match.
        
User Interests: "{user_interests}"

Available Events:
{events_text}

Please respond in JSON format with an array of recommendations. For each recommendation include:
- eventId (the index number from the list, starting from 1)
- matchScore (1-100, how well it matches user interests)
- reason (a brief explanation of why this event matches)

Return top 3 recommendations sorted by matchScore in descending order.

Example format:
{{
  "recommendations": [
    {{
      "eventId": 1,
      "matchScore": 95,
      "reason": "This event directly aligns with your interest in..."
    }}
  ]
}}

Return ONLY the JSON response without any additional text."""
        # Call Gemini API
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={settings.GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(
            gemini_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        print(response)
        
        if response.status_code != 200:
            return Response(
                {'error': 'Failed to get recommendations from AI service.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Parse response
        response_data = response.json()
        response_text = response_data['candidates'][0]['content']['parts'][0]['text']
        
        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        
        if not json_match:
            return Response(
                {'error': 'Failed to parse recommendations.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        recommendations = json.loads(json_match.group(0))
        
        return Response(recommendations, status=status.HTTP_200_OK)
        
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': 'Failed to connect to AI service.'}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        return Response(
            {'error': 'An unexpected error occurred.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    




def generate_qr_code(registration):

    #create qr code data
    qr_data=f"EVENT:{registration.event.id}|CODE:{registration.registration_code}|USER:{registration.user.id}"
    
    #generate qr code
    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    #create image
    img=qr.make_image(fill_color="pink",back_color="white")

    buffer=BytesIO()
    img.save(buffer,format='PNG')
    buffer.seek(0)

    # save to model

    filename=f"qr_{registration.registration_code}.png"
    registration.qr_code.save(filename,ContentFile(buffer.read()),save=True)

    return registration


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_for_event(request,event_id):
    try:
        event=Event.objects.get(id=event_id)

        #check if event is full
        if event.is_full:
            return Response({'error':'Event is full'},status=status.HTTP_400_BAD_REQUEST)
        
        #check if user already registered
        if Registration.objects.filter(user=request.user,event=event).exists():
            return Response({'error':'Already registered for this event'},status=status.HTTP_400_BAD_REQUEST)
        
        #check if event is past
        if event.is_past:
            return Response({'error':'Cannot register for past events'},status=status.HTTP_400_BAD_REQUEST)
        
        registration=Registration.objects.create(user=request.user,event=event)
        generate_qr_code(registration)
        serializer=RegistrationSerializer(registration)
        return Response({'message':'Registration successful','registration':serializer.data},status=status.HTTP_201_CREATED)
    except Event.DoesNotExist:
        return Response({'error':'Event not found'},status=status.HTTP_404_NOT_FOUND)   
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unregister_from_event(request,event_id):
    try:
        registration=Registration.objects.get(user=request.user,event_id=event_id)
        registration.delete()
        return Response({'message':'Unregistered successfully'},status=status.HTTP_204_NO_CONTENT)
    except Registration.DoesNotExist:
        return Response({'error':'Registration not found'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)