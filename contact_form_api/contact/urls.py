from django.urls import path
from .views import ContactFormView, MessageListView, message_list_page

urlpatterns = [
    path('contact/', ContactFormView.as_view(), name='contact-form'),
    path('messages/', MessageListView.as_view(), name='message-list'),  # API endpoint
    path('messages-page/', message_list_page, name='messages-page'),     # HTML page URL
]
