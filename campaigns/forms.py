# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django import forms

from accounts.forms import BootstrapFormMixin

from .models import Campaign


class CampaignForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Campaign
        # dm, players and invite_code are set by the views, never by the user
        fields = ["name", "setting", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
        help_texts = {
            "setting": "The world or region, e.g. Forgotten Realms.",
        }


class JoinCampaignForm(BootstrapFormMixin, forms.Form):
    invite_code = forms.CharField(max_length=16, label="Invite code")
