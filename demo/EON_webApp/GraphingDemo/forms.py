from django import forms

class GraphForm(forms.Form):
    graph_title = forms.CharField(label='Graph title', max_length=30)
    x_axis = forms.CharField(label='X-axis title', max_length=20)
    y_axis = forms.CharField(label='Y-axis title', max_length=20)
    description = forms.CharField(widget=forms.Textarea,label='Description', max_length=100)
    param1 = forms.CharField(label='1st Parameter',max_length=25)
    param2 = forms.CharField(label='2nd Parameter',max_length=25)
    param3 = forms.CharField(label='3rd Parameter',max_length=25)
    param4 = forms.CharField(label='4th Parameter',max_length=25)
    param5 = forms.CharField(label='5th Parameter',max_length=25)
    param6 = forms.CharField(label='6th Parameter',max_length=25)
    param7 = forms.CharField(label='7th Parameter',max_length=25)
    file = forms.FileField(label='Upload file')
