from django import forms



TRUE_FALSE_CHOICES = (
    (True, 'Members'),
    (False, 'Public')
)


#Form for users to fill when creating a new group
class GroupForm(forms.Form):
    #The following widget makes a given forms.CharField() only accept
    # Alphanumeric characters.
    #widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z]+', 'title':'Enter Characters Only '})
    name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9A-Za-z_]+', 'title':'Enter Characters and underscores Only '}))

    about = forms.CharField(max_length=1000, help_text='1000 characters max.')
