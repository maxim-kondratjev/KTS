from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from core.forms import LoginForm, MessageCreateForm, ChatRegistrationForm
from core.models import Message

from django.contrib.auth import get_user_model

User = get_user_model()


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'core/chat.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        last_id = self.request.GET.get("last_id")

        if last_id:
            messages = Message.objects.filter(id__gt=last_id).order_by('-id')[:20]
        else:
            messages = Message.objects.all().order_by('-id')

        data['messages'] = messages
        data['avatars'] = User.objects.filter(username__in=data['messages'].values_list('author')).all()
        data['users_avatars'] = data['avatars'].values_list('username', flat=True).exclude(avatar='')
        return data


class ChatLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_action'] = reverse('core:login')
        return data

    def get_success_url(self):
        return reverse('core:chat_get')


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/messages.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        last_id = self.request.GET.get('last_id')
        if last_id:
            messages = Message.objects.filter(id__gt=last_id).order_by('-id')[:20]
        else:
            messages = Message.objects.all().order_by('-id')
        data['messages'] = messages
        data['avatars'] = User.objects.filter(username__in=data['messages'].values_list('author')).all()
        data['users_avatars'] = data['avatars'].values_list('username', flat=True).exclude(avatar='')
        return data


class MessageCreateView(CreateView):
    form_class = MessageCreateForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('core:chat_get')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponse('Ошибка')

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse('')


class ChatLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('core:login'))


class ChatRegistrationView(CreateView):      #not used
    form_class = ChatRegistrationForm
    template_name = "core/registration.html"

    def get_success_url(self):
        return reverse('core:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def register_user(request):
    if request.method == 'POST':
        form = ChatRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:chat_get'))
        else:
            return HttpResponse("123")

    else:
        form = ChatRegistrationForm()
        return render(request, 'core/registration.html', {'form': form})


class RegisterUser(CreateView):
    form_class = ChatRegistrationForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('core:chat_get')

    def form_invalid(self, form):
        return HttpResponse('Invalid form')

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(reverse('core:login'))



