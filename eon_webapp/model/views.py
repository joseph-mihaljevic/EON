from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .forms import ModelViewForm,GraphSpecifyForm
from .models import UserModel
from .models import User

import os
import zipfile
import random
import subprocess
import json
import pandas as pd

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
    fields = ['model_name','description','code_language','executable_file_name','parameter_defaults']
    template_name = 'model/UserModel_Create.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["text_fields"]=['model_name','description','executable_file_name','parameter_defaults']
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



class GraphSpecifyDetailedUserModel(generic.DetailView):
    model = UserModel
    context_object_name = "UserModel" #use this in the template
    template_name = 'model/Display_UserModel.html'
    def get_queryset(self):
        return UserModel.objects.all()
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["url_path"] = "/model/UpdateGraphJson/"+str(data["UserModel"].id)
        data["owner_name"] = User.objects.get(pk=data["UserModel"].owner_id).username
        data['form']=GraphSpecifyForm(data["UserModel"])
        # TODO: CHANGE THIS TO LOGGING
        # runs the code in firejail within the directory
        print("RUNNING CODE")
        if os.path.exists(data["UserModel"].folder_location+"/output.csv"):
            os.remove(data["UserModel"].folder_location+"/output.csv")
        params=data["UserModel"].parameter_defaults.split(" ")
        run_command=["firejail","--private="+data["UserModel"].folder_location,"./"+data["UserModel"].executable_file_name]
        run_command+=params
        subprocess.run(run_command)
        # output is now in output.csv (should be anyway...)
        # TODO: catch error if output.csv doesn't exist
        with open(data["UserModel"].folder_location+"/output.csv") as output_file:
            output = output_file.readlines()
        output = [x.strip() for x in output]
        header = output[0].split(",")
        # data_dict = {}
        # for head in header:
        #     data_dict[head]=[]
        # for line in output[1:]:
        #     line_contents=line.split(",")
        #     for index,head in enumerate(header):
        #         data_dict[head].append(line_contents[index])
        # data["col1"]=data_dict[header[0]]
        # data["col2"]=data_dict[header[1]]
        data["output"]=output
        return data

class GraphSpecifyFormView(FormView):
    form_class=GraphSpecifyForm
    success_url=reverse_lazy('model_index')
    template_name='home.html'

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

def update_graph_json(request,model_id):
    if request.method == 'POST':
        input_field_list = str(request.body.decode("utf-8")).split('&')[1:]
        json_dict = {}
        json_dict["parameters"]={}
        json_dict["graphs"]={}
        for index,input_field in enumerate(input_field_list):
            field,input=input_field.split("=")
            if "param" in field:
                json_dict["parameters"][field]=input
            if "graph_title" in field:
                x_axis=input_field_list[index+1].split("=")[1]
                y_axis=input_field_list[index+2].split("=")[1]
                json_dict["graphs"]["graph"]={"x_axis":x_axis,"y_axis":y_axis,"name":input}
        print(json_dict)
        model=UserModel.objects.get(pk=model_id)
        with open('%s/specification.json'%str(model.folder_location), 'w+') as fp:
            json.dump(json_dict, fp)
        print(model.folder_location)
    return redirect("view_user_model",pk=model_id)

def view_user_model(request,pk):
    model = UserModel.objects.get(pk=pk)
    context={"id":pk,"url_path":"/model/View/%i/"%pk}
    default_params=model.parameter_defaults.split(" ")
    if request.method=='POST':
        params_changed=str(request.body.decode("utf-8")).split('&')[1:]
        params_for_code_list=[]
        for index,param in enumerate(default_params):
            for param_changed in params_changed:
                if str(index) in param_changed.split("=")[0]:
                    param = param_changed.split("=")[1]
            params_for_code_list.append(param)
        if os.path.exists(model.folder_location+"/output.csv"):
            os.remove(model.folder_location+"/output.csv")
        run_command=["firejail","--private="+model.folder_location,"./"+model.executable_file_name]
        run_command+=params_for_code_list
        subprocess.run(run_command)
    folder_location = str(model.folder_location)
    csv_location = "%s/output.csv"%folder_location
    json_location = "%s/specification.json"%folder_location
    with open(json_location, 'r') as json_f:
        specification_dict = json.load(json_f)
    # with open(csv_location, 'r') as csv_f:
    df = pd.read_csv(csv_location)
    df.rename(inplace=True,columns=lambda x: x.strip())
    x_axis = list(df[specification_dict["graphs"]["graph"]["x_axis"]].values)
    y_axis = list(df[specification_dict["graphs"]["graph"]["y_axis"]].values)
    context["x_axis"]=x_axis
    context["y_axis"]=y_axis
    context["graph_name"]=specification_dict["graphs"]["graph"]["name"].replace("+"," ")
    parameters=[]
    for index,parameter in enumerate(default_params):
        upper_bound=specification_dict["parameters"]["param_%i_upper_bound"%index]
        lower_bound=specification_dict["parameters"]["param_%i_lower_bound"%index]
        if upper_bound!=lower_bound:
            parameters.append({"name":"param_%i"%index,"default":parameter,
            "upper_bound":upper_bound,
            "lower_bound":lower_bound,
            "step":(float(upper_bound)-float(lower_bound))/10000,})
    context["parameters"]=parameters
    return render(request, 'model/view_user_model.html',context)

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
