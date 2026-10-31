# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django import forms

from accounts.forms import BootstrapFormMixin

from .models import NPC, Campaign, GameSession


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


class GameSessionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = GameSession
        # campaign is set by the view, never by the user
        fields = ["number", "title", "date_played", "recap", "dm_notes"]
        widgets = {
            "date_played": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "recap": forms.Textarea(attrs={"rows": 8}),
            "dm_notes": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "dm_notes": "Only you can see these notes.",
        }

    def __init__(self, *args, campaign, **kwargs):
        super().__init__(*args, **kwargs)
        self.campaign = campaign

    def clean_number(self):
        # campaign isn't a form field, so Django skips the unique check on its own
        number = self.cleaned_data["number"]
        duplicates = GameSession.objects.filter(campaign=self.campaign, number=number)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError(f"Session {number} already exists in this campaign.")
        return number


class NPCForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = NPC
        # campaign is set by the view, never by the user
        fields = ["name", "race", "role", "status", "description", "secret_notes", "is_hidden"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "secret_notes": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "secret_notes": "Only you can see these notes.",
        }
