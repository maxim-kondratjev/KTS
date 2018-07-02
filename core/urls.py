from django.conf.urls import url
from django.urls import path

from core.views import ChatView, ChatLoginView, MessageCreateView, ChatLogoutView, ChatRegistrationView, MessagesView, \
    register_user, RegisterUser

urlpatterns = [
    url(r'get$', ChatView.as_view(), name='chat_get'),
    path('login/', ChatLoginView.as_view(), name='login'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('logout/', ChatLogoutView.as_view(), name='logout'),
    path('registration/', register_user, name='registration'),
    path('register_user/', RegisterUser.as_view(), name='register_user'),
    path('messages/', MessagesView.as_view(), name='messages'),
]
