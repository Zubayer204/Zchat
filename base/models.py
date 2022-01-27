from django.db import models

# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.room_name


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name
