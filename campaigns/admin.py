# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django.contrib import admin

from .models import NPC, Campaign, GameSession


class GameSessionInline(admin.TabularInline):
    model = GameSession
    extra = 0
    fields = ("number", "title", "date_played")
    show_change_link = True


class NPCInline(admin.TabularInline):
    model = NPC
    extra = 0
    fields = ("name", "race", "role", "status", "is_hidden")
    show_change_link = True


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "dm", "player_count", "created_at")
    search_fields = ("name", "dm__username")
    filter_horizontal = ("players",)
    readonly_fields = ("invite_code", "created_at")
    inlines = (GameSessionInline, NPCInline)

    @admin.display(description="Players")
    def player_count(self, obj):
        return obj.players.count()


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "campaign", "number", "date_played")
    list_filter = ("campaign",)
    search_fields = ("title", "recap")
    date_hierarchy = "date_played"
    fieldsets = (
        (None, {"fields": ("campaign", "number", "title", "date_played")}),
        ("Recap", {"fields": ("recap",)}),
        ("DM Secrets", {"classes": ("collapse",), "fields": ("dm_notes",)}),
    )


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ("name", "campaign", "race", "role", "status", "is_hidden")
    list_filter = ("campaign", "status", "is_hidden")
    search_fields = ("name", "role")
    list_editable = ("status",)
    fieldsets = (
        (None, {"fields": ("campaign", "name", "race", "role", "status")}),
        ("Description", {"fields": ("description",)}),
        ("DM Secrets", {"classes": ("collapse",), "fields": ("secret_notes", "is_hidden")}),
    )
