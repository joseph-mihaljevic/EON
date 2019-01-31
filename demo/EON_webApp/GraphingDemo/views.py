from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import GraphForm
from django.urls import reverse
import os
# Create your views here.


def Index(request):
    #return HttpResponse("<h2>HEY!</h2>")
    return render(request,'GraphingDemo/Home.html')

def UploadCode(request):
    form = GraphForm()

    return render(request, 'GraphingDemo/UploadCode.html', {'form':form})

def RunCode(request):

    #return HttpResponse("<h2>HEY!</h2>")
    return render(request,'GraphingDemo/RunCode.html')

def DisplayGraph(request):
    print("'",request.method,"'")
    form1 = GraphForm()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GraphForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            context = request.POST.dict()
            params = [context['param1'],context['param2'],context['param3'],context['param4'],context['param5'],context['param6'],context['param7']]
            parsed_params=[None]*len(params)
            for index,param in enumerate(params):
                print(str(param),index)
                parsed_params[index] = param[0]
            run_code(request.FILES['file'],params)
            context['file'] = request.FILES['file']
            context['code'] = handle_uploaded_file(request.FILES.get('file'))
            context['form'] = form
            print("context,",context)
            return render(request,'GraphingDemo/DisplayGraph.html', context)
    elif request.method == 'GET':
        print("GET Detected",request.GET)
        # create a form instance and populate it with data from the request:

        # check whether it's valid:
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        form = GraphForm(request.GET, request.FILES)
        context = request.GET.dict()
        print("context,",context)
        params = [context['param1'],context['param2'],context['param3'],context['param4'],context['param5'],context['param6'],context['param7']]
        parsed_params=[None]*len(params)
        for index,param in enumerate(params):
            print(str(param),index)
            parsed_params[index] = param[0]
        Only_run_code(params)
        context['form'] = form
        return render(request,'GraphingDemo/DisplayGraph.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        print("Made it here!")
        return HttpResponseRedirect('UploadCode')



def DisplayGraph_Test(request):
    return render(request,'GraphingDemo/DisplayGraph.html')



def handle_uploaded_file(f):
    data = str(f.read())
    return data

def run_code(f,params):
    # clean sandbox
    os.system('rm -f GraphingDemo/static/private_directory/output.csv')
    os.system('rm -f GraphDemo/static/private_directory/user_code')
    # save the file to a local directory
    with open('GraphingDemo/static/private_directory/user_code', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # run the code
    os.system('chmod +rwx GraphingDemo/static/private_directory/user_code')
    command = 'firejail --private=GraphingDemo/static/private_directory ./user_code'
    for param in params:
        command+= " "
        command+= param
    print(command)
    os.system(command)

def Only_run_code(params):
    # clean sandbox
    os.system('rm -f GraphingDemo/static/private_directory/output.csv')

    os.system('chmod +rwx GraphingDemo/static/private_directory/user_code')
    command = 'firejail --private=GraphingDemo/static/private_directory ./user_code'
    for param in params:
        command+= " "
        command+= param
    print(command)
    os.system(command)
