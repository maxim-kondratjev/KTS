from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect, request, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, FormView

from core.forms import LoginForm, MessageCreateForm, ChatRegistrationForm
from core.models import Message


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
        return HttpResponseRedirect(reverse('core:chat_get'))

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({
            'id': self.object.id,
            'text': self.object.text,
            'author': self.object.author.username,
            'date': self.object.date,
            'rendered_template': render_to_string('core/message.html', {'m': self.object}, self.request)
        })


class ChatLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('core:login'))


class ChatRegistrationView(FormView):
    form_class = ChatRegistrationForm
    template_name = "core/registration.html"

    def get_success_url(self):
        return reverse('core:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
