from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import ModelViewForm
from .models import UserModel

class Index(generic.ListView):
    #UserModel.objects.get(author_PK=User.pk)
    if(True):
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
    context = {}
    context["ModelViewForm"] = ModelViewForm()
    model = UserModel

    fields = ['model_name','description','EONid','uploaded_code']
    template_name = 'model/Update_UserModel.html'


class UserModelDelete(DeleteView):
    model = UserModel
    context_object_name = "UserModel" #use this in the template
    success_url = reverse_lazy('model_index')
    template_name = 'model/UserModel_confirm_delete.html'



    #context_object_name = "UserModel"
class CreateModelView(UpdateView):
    fields = ['model_name','description','EONid','uploaded_code']
    template_name = 'model/Update_UserModel.html'
    print(UserModel.model_name)


    success_url = ('Display-UserModel')
    template_name = 'ModelView_form.html'

    def get_queryset(self):
        return UserModel.objects.all()

class UpdateModelView(UpdateView):
    model = UserModel
    fields = ['model_name','description','EONid','uploaded_code']

    #context_object_name = "UserModel"
    template_name = 'model/Update_UserModel.html'
    print(UserModel.model_name)


    success_url = ('Display-UserModel')
    template_name = 'ModelView_form.html'

    def get_queryset(self):
        return UserModel.objects.all()


def CreateModelViewForm(request):
    form = ModelViewForm()
    if request.method == 'POST':
        print("Post")
        #form = ModelViewForm(request.POST, request.FILES)
        return render(request, 'model/Display_UserModelView.html', {'form': form})
    else:
        return render(request, 'model/Display_UserModelView.html', {'form': form})


class UpdateModelViewForm(UpdateView):
    def UpdateModelViewForm(self):
        return











#
