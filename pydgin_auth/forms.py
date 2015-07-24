from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from pydgin_auth.models import UserProfile


class PydginUserCreationForm(UserCreationForm):
    is_terms_agreed = forms.BooleanField(label="Terms and conditions", required=True)
    email = forms.EmailField(label="Email address", max_length=254, required=True)

    class Meta:
        model = User
        # fields = ("username", "email", "password1", "password2", "is_terms_agreed")
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(PydginUserCreationForm, self).save(commit=True)
        # user_profile = UserProfile(user=user, is_terms_agreed=self.cleaned_data['is_terms_agreed'])
        user_profile = UserProfile(user=user)
        user_profile.save()
        return user_profile
