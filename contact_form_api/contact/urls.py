from django.urls import path
from .views import (
    ContactFormView,
    MessageListView,
    message_list_page,
    HireRequestView
)

urlpatterns = [
    # Web Page
    path('messages-page/', message_list_page, name='messages-page'),
    
    # API Endpoints
    path('contact/', ContactFormView.as_view(), name='contact-form'),
    path('api/messages/', MessageListView.as_view(), name='message-list'),
    path('hire-requests', HireRequestView.as_view(), name='hire-requests'),
]