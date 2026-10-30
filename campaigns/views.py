# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CampaignForm, JoinCampaignForm
from .models import Campaign


def get_member_campaign(request, pk):
    """Return the campaign if the user is its DM or a player, otherwise 404."""
    campaigns = Campaign.objects.filter(
        Q(dm=request.user) | Q(players=request.user)
    ).distinct()
    return get_object_or_404(campaigns, pk=pk)


def get_dm_campaign(request, pk):
    """Return the campaign only if the user is its DM, otherwise 404."""
    return get_object_or_404(Campaign, pk=pk, dm=request.user)


def home(request):
    return render(request, "campaigns/home.html")


@login_required
def campaign_list(request):
    context = {
        "campaigns_run": request.user.campaigns_run.all(),
        "campaigns_joined": request.user.campaigns_joined.select_related("dm"),
        "join_form": JoinCampaignForm(),
    }
    return render(request, "campaigns/campaign_list.html", context)


@login_required
def campaign_detail(request, pk):
    campaign = get_member_campaign(request, pk)
    context = {
        "campaign": campaign,
        "is_dm": campaign.is_dm(request.user),
        "players": campaign.players.all(),
    }
    return render(request, "campaigns/campaign_detail.html", context)


@login_required
def campaign_create(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.dm = request.user
            campaign.save()
            messages.success(request, f"Created {campaign.name}. Share the invite code with your players.")
            return redirect("campaign_detail", pk=campaign.pk)
    else:
        form = CampaignForm()

    return render(request, "campaigns/campaign_form.html", {"form": form})


@login_required
def campaign_edit(request, pk):
    campaign = get_dm_campaign(request, pk)
    if request.method == "POST":
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, "Campaign updated.")
            return redirect("campaign_detail", pk=campaign.pk)
    else:
        form = CampaignForm(instance=campaign)

    return render(request, "campaigns/campaign_form.html", {"form": form, "campaign": campaign})


@login_required
@require_POST
def campaign_delete(request, pk):
    campaign = get_dm_campaign(request, pk)
    name = campaign.name
    campaign.delete()
    messages.success(request, f"Deleted {name}.")
    return redirect("campaign_list")


@login_required
@require_POST
def campaign_join(request):
    form = JoinCampaignForm(request.POST)
    campaign = None
    if form.is_valid():
        campaign = Campaign.objects.filter(
            invite_code=form.cleaned_data["invite_code"]
        ).first()

    if campaign is None:
        messages.error(request, "Invalid invite code.")
        return redirect("campaign_list")

    if campaign.is_member(request.user):
        messages.info(request, f"You're already part of {campaign.name}.")
    else:
        campaign.players.add(request.user)
        messages.success(request, f"You joined {campaign.name}!")
    return redirect("campaign_detail", pk=campaign.pk)
