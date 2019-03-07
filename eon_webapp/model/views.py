from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import ModelViewForm
from .models import UserModel
from .models import User
import os
import zipfile
import random
import subprocess

CODE_REPOSITORIES_PATH="/home/joe/EON/eon_webapp/model_code"

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
    fields = ['model_name','description','code_language','executable_file_name']
    template_name = 'model/UserModel_Create.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["text_fields"]=['model_name','description','executable_file_name']
        data["languages"]=['C','Python']
        data["dropdown_fields"]=["code_language"]
        return data
    def form_valid(self, form):
        user_model = form.save(commit=False)
        user_model.owner = self.request.user
        # TODO: ensure that folder location doesnt clash! usually not an issue but COULD happen
        model_folder_location = CODE_REPOSITORIES_PATH+"/"+str(user_model.owner) + "_"+str(random.randint(0,999999))
        user_model.folder_location=model_folder_location
        # Create folder for user code, then copy the file from memory to folder
        os.mkdir(model_folder_location)
        user_code = self.request.FILES["fileToUpload"]
        with open(model_folder_location+"/zipped_code.zip", 'wb+') as destination:
            for chunk in user_code.chunks():
                destination.write(chunk)
        # unzip the files in place
        with zipfile.ZipFile(model_folder_location+"/zipped_code.zip", 'r') as zipped_code:
            zipped_code.extractall(model_folder_location)
        os.remove(model_folder_location+"/zipped_code.zip") #zip not needed after extraction
        return super(CreateUserModel, self).form_valid(form)

    #context_object_name = "UserModel"



class DetailedUserModel(generic.DetailView):
    model = UserModel
    context_object_name = "UserModel" #use this in the template
    template_name = 'model/Display_UserModel.html'
    def get_queryset(self):
        return UserModel.objects.all()
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["owner_name"] = User.objects.get(pk=data["UserModel"].owner_id).username
        # TODO: CHANGE THIS TO LOGGING v
        # runs the code in firejail within the directory
        print("RUNNING CODE")
        run_command=["firejail","--private="+data["UserModel"].folder_location,"./"+data["UserModel"].executable_file_name,
        "50",
        "1.5",
        ".5",
        ".07692307692",
        ".00005479452",
        ".75",
        ".25"]
        subprocess.run(run_command)
        # output is now in output.csv (should be anyway...)
        # TODO: catch error if output.csv doesn't exist
        with open(data["UserModel"].folder_location+"/output.csv") as output_file:
            output = output_file.readlines()
        output = [x.strip() for x in output]
        data["output"]=output
        return data


class UpdateUserModel(UpdateView):
    context = {}
    context["ModelViewForm"] = ModelViewForm()
    model = UserModel

    fields = ['model_name','description','executable_file_name']
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
