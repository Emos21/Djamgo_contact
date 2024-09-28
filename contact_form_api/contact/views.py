from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import Contact
from .serializers import ContactSerializer

# View to handle form submission
class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact_instance = serializer.save()
            return Response({
                "success": "Contact form submitted successfully",
                "data": {
                    "name": contact_instance.name,
                    "email_or_phone": contact_instance.email_or_phone,
                    "message": contact_instance.message
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to retrieve all submitted messages
class MessageListView(ListAPIView):
    queryset = Contact.objects.all().order_by('-created_at')  # Fetch all messages in descending order
    serializer_class = ContactSerializer


# View to render the HTML page displaying the messages
def message_list_page(request):
    return render(request, 'messages.html')
