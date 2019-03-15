from django import forms

from .models import UserModel


class ModelViewForm(forms.Form):
    graph_title = forms.CharField(label='Graph title', max_length=30)
    x_axis = forms.CharField(label='X-axis title', max_length=20)
    y_axis = forms.CharField(label='Y-axis title', max_length=20)
    description = forms.CharField(widget=forms.Textarea,label='Description', max_length=100)
    param1 = forms.CharField(label='1st Parameter',max_length=25)
    param2 = forms.CharField(label='2nd Parameter',max_length=25)

class GraphSpecifyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if len(args):
            if str(type(args[0]))=="<class 'model.models.UserModel'>":
                super().__init__()
                params_list=args[0].parameter_defaults.split(" ")
                for index,param in enumerate(params_list):
                    self.fields["param_%i_upper_bound"%index]=forms.CharField(label="Param %i upper bound"%index,max_length=30,initial=str(param))
                    self.fields["param_%i_lower_bound"%index]=forms.CharField(label="Param %i lower bound"%index,max_length=30,initial=str(param))
                self.fields["graph_title"] = forms.CharField(label='Graph title', max_length=30)
                self.fields["x_axis"] = forms.CharField(label='X-axis title', max_length=20)
                self.fields["y_axis"] = forms.CharField(label='Y-axis title', max_length=20)
            else:
                super(GraphSpecifyForm,self).__init__(*args,**kwargs)
        else:
            super(GraphSpecifyForm,self).__init__(*args,**kwargs)
