# views.py
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import Contact, HireRequest
from .serializers import ContactSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re
import logging


# Initialize logger
logger = logging.getLogger(__name__)

class ContactFormView(APIView):
    """
    Handle contact form submissions with email notification
    """
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Save contact instance
            contact = serializer.save()

            # Prepare email content
            email_content = f"""
            New Contact Form Submission:
            
            Name: {contact.name}
            Contact: {contact.email_or_phone}
            Message: {contact.message}
            
            Received at: {contact.created_at}
            """

            # Send notification email
            send_mail(
                subject=f"New message from {contact.name}",
                message=email_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_TO_EMAIL],
                fail_silently=False
            )

            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as error:
            logger.error(f"Contact form error: {str(error)}", exc_info=True)
            return Response({
                "status": "error",
                "message": "Failed to process request"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class HireRequestView(APIView):
    """
    Handle hire request submissions with database storage and email notification
    """
    def post(self, request):
        email = request.data.get('email', '').strip()
        service = request.data.get('service', '').strip().lower()

        # Validate inputs
        validation_error = self._validate_request(email, service)
        if validation_error:
            return validation_error

        try:
            # Create database record
            HireRequest.objects.create(email=email, service_needed=service)

            # Send notification email
            self._send_notification_email(email, service)

            return Response(
                {"status": "success"}, 
                status=status.HTTP_201_CREATED
            )

        except Exception as error:
            logger.error(f"Hire request error: {str(error)}", exc_info=True)
            return Response({
                "status": "error",
                "message": "Internal server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_request(self, email, service):
        """Centralized validation logic"""
        if not email or not service:
            return Response({
                "status": "error",
                "message": "Email and service selection are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return Response({
                "status": "error",
                "message": "Invalid email format"
            }, status=status.HTTP_400_BAD_REQUEST)

        if service not in {'graphic', 'web', 'both'}:
            return Response({
                "status": "error",
                "message": "Invalid service selection"
            }, status=status.HTTP_400_BAD_REQUEST)

        return None

    def _send_notification_email(self, email, service):
        """Send formatted notification email"""
        email_content = f"""
        New Service Request Received:
        
        Client Email: {email}
        Requested Service: {service.title()}
        
        You can reply directly to this email to contact the client.
        """

        send_mail(
            subject=f"New {service.title()} Service Request",
            message=email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_TO_EMAIL],
            reply_to=[email],
            fail_silently=False
        )


class MessageListView(ListAPIView):
    """
    Retrieve all contact messages in chronological order
    """
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer


def message_list_page(request):
    """
    Render HTML template for viewing messages
    """
    return render(request, 'messages.html')