from django.forms import JSONField
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RoomMember
from .models import Room
from agora_token_builder import RtcTokenBuilder
from random import randint
import time
import json
from datetime import timezone
from datetime import datetime

# Create your views here.

def getToken(request):
    app_id = "ccc90dbecbb0476e83bfa98456c31a0c"
    app_certificate = "7b03b288cc24480789355b3b15d7cbd3"
    channel_name = request.GET.get('channel')
    uid = randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilageExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilageExpiredTs)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')


def room(request):
    return render(request, 'base/room.html')


def get_member(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    room = Room.objects.get(
        room_name=room_name
    )

    member = RoomMember.objects.get(
        uid=uid,
        room=room
    )

    name = member.name
    return JsonResponse({'error': False, 'name': name}, safe=False)


@csrf_exempt
def delete_member(request):
    data = json.loads(request.body)

    room = Room.objects.get(
        room_name=data['room_name']
    )

    member = RoomMember.objects.get(
        uid = data['UID'],
        name=data['name'],
        room=room
    )
    
    member.delete()
    return JsonResponse({'error': False, 'name': data['name']}, safe=False)

@csrf_exempt
def enter_room(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            room = Room.objects.get(
                room_name=data['room_name'],
                password=data['password']
            )

            dt_prev = room.created_on
            dt_now  = datetime.now(timezone.utc)
            diff = dt_now - dt_prev
            if (diff.seconds // 3600) >= 24:
                room.delete()
                return JsonResponse({'error': True, 'message': "*Room expired. Please create a new one."}, safe=False)
            
            member, created = RoomMember.objects.get_or_create(
                name = data['name'],
                uid = data['UID'],
                room=room
            )
            return JsonResponse({'error': False, 'name': data['name']}, safe=False)

        except Room.DoesNotExist:
        
            return JsonResponse({'error': True, 'message': "*Room name or password didn't match"}, safe=False)


@csrf_exempt
def create_room(request):
    data = json.loads(request.body)
    try:
        room = Room.objects.get(
            room_name=data['room_name']
        )
        return JsonResponse({'error': True, 'message': '*Room exists. Use different room name'}, safe=False)
    except Room.DoesNotExist:
        pass

    room = Room.objects.create(
        room_name=data['room_name'],
        password=data['password']
    )

    member = RoomMember.objects.create(
        name=data['name'],
        uid=data['UID'],
        room=room
    )

    return JsonResponse({"error": False, "room_id": room.id})
