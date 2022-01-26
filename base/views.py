from django.forms import JSONField
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RoomMember
from agora_token_builder import RtcTokenBuilder
from random import randint
import time
import json

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


@csrf_exempt
def create_user(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name': data['name']}, safe=False)


def get_member(request):
    uid = request.GET.get('uid')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name
    )

    name = member.name
    return JsonResponse({'name': name}, safe=False)


@csrf_exempt
def delete_member(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        uid = data['UID'],
        name=data['name'],
        room_name=data['room_name']
    )
    
    member.delete()
    return JsonResponse({'name': data['name']}, safe=False)
