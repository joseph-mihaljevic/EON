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
    #model.created_by = request.user
    fields = ['model_name','description']
    template_name = 'model/UserModels_form.html'
    #context_object_name = "UserModel"



class DetailedUserModel(generic.DetailView):
    model = UserModel
    context_object_name = "UserModel" #use this in the template
    template_name = 'model/Display_UserModel.html'
    def get_queryset(self):
        return UserModel.objects.all()


class UpdateUserModel(UpdateView):
    model = UserModel
    fields = ['model_name','description','EONid','uploaded_code']
    template_name = 'model/Update_UserModel.html'


class UserModelDelete(DeleteView):
    model = UserModel
    context_object_name = "UserModel" #use this in the template
    success_url = reverse_lazy('model_index')
    template_name = 'model/UserModel_confirm_delete.html'



class GraphicalView(generic.View):
    #form_class = PostCreationForm
    fields = ['model_name','description']
    template_name = 'model/Display_UserModel.html'
