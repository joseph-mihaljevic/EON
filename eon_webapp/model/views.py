from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView

from .models import UserModel

class Index(generic.ListView):
    model = UserModel
    template_name = "model/index.html"
    context_object_name = "UserModels" #use this in the template
    fields = []
    def get_queryset(self):
        return UserModel.objects.all()

    #def detail(request,):


class CreateUserModel(CreateView):
    model = UserModel
    fields = ['model_name','description']
    template_name = 'model/UserModels_form.html'

class DetailedUserModel(generic.DetailView):
    model = UserModel
    context_object_name = "UserModel" #use this in the template
    template_name = 'model/Display_UserModel.html'
    def get_queryset(self):
        return UserModel.objects.all()


class UpdateUserModel(UpdateView):
    model = UserModel
    fields = ['model_name','description']
    template_name = 'model/Update_UserModel.html'

class DeleteUserModel(DeleteView):
    model = reverse_lazy('')
