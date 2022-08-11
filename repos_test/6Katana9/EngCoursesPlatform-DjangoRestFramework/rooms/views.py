from .serializers import RoomSerializer
from .models import Room
from rest_framework import viewsets, permissions
    

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


    def perform_create(self, serializer):
        serializer.save(room_user=self.request.user)
        

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context