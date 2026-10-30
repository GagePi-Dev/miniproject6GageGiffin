# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

import secrets

from django.conf import settings
from django.db import models


def generate_invite_code():
    # 12 random URL-safe characters, hard to guess
    return secrets.token_urlsafe(9)


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    setting = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    dm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns_run",
        verbose_name="DM",
    )
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="campaigns_joined",
    )
    invite_code = models.CharField(
        max_length=16,
        unique=True,
        default=generate_invite_code,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def is_dm(self, user):
        return user.is_authenticated and self.dm_id == user.pk

    def is_member(self, user):
        if not user.is_authenticated:
            return False
        return self.is_dm(user) or self.players.filter(pk=user.pk).exists()


class GameSession(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="sessions"
    )
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    date_played = models.DateField()
    recap = models.TextField()
    dm_notes = models.TextField("DM notes", blank=True)

    class Meta:
        ordering = ["number"]
        verbose_name = "game session"
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "number"], name="unique_session_number"
            )
        ]

    def __str__(self):
        return f"{self.campaign} - Session {self.number}: {self.title}"


class NPC(models.Model):
    class Status(models.TextChoices):
        ALIVE = "alive", "Alive"
        DEAD = "dead", "Dead"
        UNKNOWN = "unknown", "Unknown"

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="npcs"
    )
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.UNKNOWN
    )
    description = models.TextField(blank=True)
    secret_notes = models.TextField(blank=True)
    is_hidden = models.BooleanField(
        default=False, help_text="Hidden NPCs are only visible to the DM."
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "NPC"
        verbose_name_plural = "NPCs"

    def __str__(self):
        return self.name
