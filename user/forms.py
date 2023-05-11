from django import forms


class TwoUsersForm(forms.Form):
    user1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username1'}),
                            max_length=500)
    user2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username2'}),
                            max_length=500)

class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
                            max_length=500)