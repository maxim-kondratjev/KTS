from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, FormView

from core.forms import LoginForm, MessageCreateForm, ChatRegistrationForm
from core.models import Message


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'core/chat.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        messages = Message.objects.all().order_by('-id')
        data['messages'] = messages
        return data

class ChatLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_action'] = reverse('core:login')
        return data

    def get_success_url(self):
        return reverse('core:chat_get')


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
        return HttpResponseRedirect(reverse('core:chat_get'))

class ChatLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('core:login'))


class ChatRegistrationView(FormView):
    form_class = ChatRegistrationForm
    template_name = "registration.html"

    def get_success_url(self):
        return reverse('core:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    """def post(self, request, *args, **kwargs):
            form = ChatRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('core:chat_get'))

        def get(self, request, *args, **kwargs):
            form = ChatRegistrationForm()
            return render(request, 'registration.html', {'form': form})"""