# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CampaignForm, GameSessionForm, JoinCampaignForm, NPCForm
from .models import NPC, Campaign, GameSession


def get_member_campaign(request, pk):
    """Return the campaign if the user is its DM or a player, otherwise 404."""
    campaigns = Campaign.objects.filter(
        Q(dm=request.user) | Q(players=request.user)
    ).distinct()
    return get_object_or_404(campaigns, pk=pk)


def get_dm_campaign(request, pk):
    """Return the campaign only if the user is its DM, otherwise 404."""
    return get_object_or_404(Campaign, pk=pk, dm=request.user)


def visible_npcs(campaign, user):
    """All NPCs for the DM; hidden NPCs are left out for players."""
    npcs = campaign.npcs.all()
    if not campaign.is_dm(user):
        npcs = npcs.filter(is_hidden=False)
    return npcs


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
        "recent_sessions": campaign.sessions.order_by("-number")[:3],
        "session_count": campaign.sessions.count(),
        "npc_count": visible_npcs(campaign, request.user).count(),
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


@login_required
def session_list(request, pk):
    campaign = get_member_campaign(request, pk)
    context = {
        "campaign": campaign,
        "is_dm": campaign.is_dm(request.user),
        "sessions": campaign.sessions.all(),
    }
    return render(request, "campaigns/session_list.html", context)


@login_required
def session_detail(request, pk, sid):
    campaign = get_member_campaign(request, pk)
    session = get_object_or_404(GameSession, pk=sid, campaign=campaign)
    context = {
        "campaign": campaign,
        "session": session,
        "is_dm": campaign.is_dm(request.user),
        "previous_session": campaign.sessions.filter(number__lt=session.number).last(),
        "next_session": campaign.sessions.filter(number__gt=session.number).first(),
    }
    return render(request, "campaigns/session_detail.html", context)


@login_required
def session_create(request, pk):
    campaign = get_dm_campaign(request, pk)
    if request.method == "POST":
        form = GameSessionForm(request.POST, campaign=campaign)
        if form.is_valid():
            session = form.save(commit=False)
            session.campaign = campaign
            session.save()
            messages.success(request, f"Added Session {session.number}.")
            return redirect("session_detail", pk=campaign.pk, sid=session.pk)
    else:
        last_number = campaign.sessions.aggregate(Max("number"))["number__max"] or 0
        form = GameSessionForm(campaign=campaign, initial={"number": last_number + 1})

    return render(request, "campaigns/session_form.html", {"form": form, "campaign": campaign})


@login_required
def session_edit(request, pk, sid):
    campaign = get_dm_campaign(request, pk)
    session = get_object_or_404(GameSession, pk=sid, campaign=campaign)
    if request.method == "POST":
        form = GameSessionForm(request.POST, instance=session, campaign=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, "Session updated.")
            return redirect("session_detail", pk=campaign.pk, sid=session.pk)
    else:
        form = GameSessionForm(instance=session, campaign=campaign)

    context = {"form": form, "campaign": campaign, "session": session}
    return render(request, "campaigns/session_form.html", context)


@login_required
@require_POST
def session_delete(request, pk, sid):
    campaign = get_dm_campaign(request, pk)
    session = get_object_or_404(GameSession, pk=sid, campaign=campaign)
    number = session.number
    session.delete()
    messages.success(request, f"Deleted Session {number}.")
    return redirect("session_list", pk=campaign.pk)


@login_required
def npc_list(request, pk):
    campaign = get_member_campaign(request, pk)
    npcs = visible_npcs(campaign, request.user)

    # Only filter on a known status value; anything else shows all NPCs
    status = request.GET.get("status")
    if status in NPC.Status.values:
        npcs = npcs.filter(status=status)
    else:
        status = None

    context = {
        "campaign": campaign,
        "is_dm": campaign.is_dm(request.user),
        "npcs": npcs,
        "status": status,
        "status_choices": NPC.Status.choices,
    }
    return render(request, "campaigns/npc_list.html", context)


@login_required
def npc_create(request, pk):
    campaign = get_dm_campaign(request, pk)
    if request.method == "POST":
        form = NPCForm(request.POST)
        if form.is_valid():
            npc = form.save(commit=False)
            npc.campaign = campaign
            npc.save()
            messages.success(request, f"Added {npc.name}.")
            return redirect("npc_list", pk=campaign.pk)
    else:
        form = NPCForm()

    return render(request, "campaigns/npc_form.html", {"form": form, "campaign": campaign})


@login_required
def npc_edit(request, pk, nid):
    campaign = get_dm_campaign(request, pk)
    npc = get_object_or_404(NPC, pk=nid, campaign=campaign)
    if request.method == "POST":
        form = NPCForm(request.POST, instance=npc)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {npc.name}.")
            return redirect("npc_list", pk=campaign.pk)
    else:
        form = NPCForm(instance=npc)

    return render(request, "campaigns/npc_form.html", {"form": form, "campaign": campaign, "npc": npc})


@login_required
@require_POST
def npc_delete(request, pk, nid):
    campaign = get_dm_campaign(request, pk)
    npc = get_object_or_404(NPC, pk=nid, campaign=campaign)
    name = npc.name
    npc.delete()
    messages.success(request, f"Deleted {name}.")
    return redirect("npc_list", pk=campaign.pk)
