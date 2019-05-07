from django import forms



TRUE_FALSE_CHOICES = (
    (True, 'Members'),
    (False, 'Public')
)

class GroupForm(forms.Form):
    name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z]+', 'title':'Enter Characters Only '}))
    about = forms.CharField(max_length=100, help_text='100 characters max.')
