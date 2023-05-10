from .models import Relations
from django.forms import ModelForm, TextInput

class RelationsForm(ModelForm):
    class Meta:
        model = Relations
        fields = ['user', 'user_friend']
        widgets = {
            'user': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username1'
            }),
            'user_friend': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username2'
            })
        }

