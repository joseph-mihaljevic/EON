from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class Index(generic.CreateView):
    template_name = 'forum/index.html'
