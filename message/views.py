from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializers


class MessageAPIView(APIView):
    
    # message post request 
    def post(self, request):
        serializer = MessageSerializers(data=request.data) 
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully!"}, status=201)
        return Response(serializer.errors, status=400)