# adapters.py
from allauth.account.adapter import DefaultAccountAdapter
import uuid

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)
        user.generate_tracking_id()  # Call the method to generate the tracking ID
        if commit:
            user.save()
        return user
