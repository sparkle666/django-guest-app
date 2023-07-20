from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
     
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.generate_tracking_id()  # Call the method to generate the tracking ID
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "tracking_id", 'email', 'username')
        exclude = ["password",]
        


   

