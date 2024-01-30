from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    username = forms.CharField(max_length=100, label="Your name")
    email = forms.EmailField(required=True, label="Your e-mail address")
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
            user = initial_arguments.get('user', None)
            if user:
                updated_initial['username'] = user.username
                updated_initial['email'] = user.email
                kwargs.update(initial=updated_initial)
        super(ContactForm, self).__init__(*args, **kwargs)