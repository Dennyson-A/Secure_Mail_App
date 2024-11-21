from django.urls import path
from .views import RegisterUser, LoginUser, SendMessage, GetMessages

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('send-message/', SendMessage.as_view(), name='send_message'),
    path('messages/', GetMessages.as_view(), name='get_messages'),
]
