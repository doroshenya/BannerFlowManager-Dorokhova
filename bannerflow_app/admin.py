from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Campaign, Banner, UserProfile, ABTest, CampaignStatistics
from .models import BannerTemplate, GameData, GeneratedBanner

# Расширение пользователя
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'start_date', 'end_date', 'status', 'target_platform', 'created_by', 'created_at')
    list_filter = ('status', 'target_platform', 'is_ab_test', 'created_at')
    search_fields = ('name', 'target_game_version')
    readonly_fields = ('created_at',)
    actions = ['activate_campaigns', 'pause_campaigns', 'stop_campaigns']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'budget', 'created_by')
        }),
        ('Временные рамки', {
            'fields': ('start_date', 'end_date')
        }),
        ('Таргетинг', {
            'fields': ('target_platform', 'target_geolocation', 'target_game_version')
        }),
        ('Статус', {
            'fields': ('status', 'is_ab_test')
        }),
    )

    def activate_campaigns(self, request, queryset):
        for campaign in queryset:
            campaign.activate()
        self.message_user(request, f"{queryset.count()} кампаний активировано")
    activate_campaigns.short_description = "Активировать выбранные кампании"

    def pause_campaigns(self, request, queryset):
        for campaign in queryset:
            campaign.pause()
        self.message_user(request, f"{queryset.count()} кампаний приостановлено")
    pause_campaigns.short_description = "Приостановить выбранные кампании"

    def stop_campaigns(self, request, queryset):
        for campaign in queryset:
            campaign.stop()
        self.message_user(request, f"{queryset.count()} кампаний остановлено")
    stop_campaigns.short_description = "Остановить выбранные кампании"

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'campaign', 'media_type', 'is_active', 'created_at')
    list_filter = ('media_type', 'is_active', 'created_at')
    search_fields = ('title', 'campaign__name')
    readonly_fields = ('created_at', 'media_type')

@admin.register(ABTest)
class ABTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'audience_segment', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'start_date')
    search_fields = ('name', 'campaign__name', 'audience_segment')
    filter_horizontal = ('banners',)

@admin.register(CampaignStatistics)
class CampaignStatisticsAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'date', 'impressions', 'clicks', 'conversions', 'ctr')
    list_filter = ('date', 'campaign')
    readonly_fields = ('ctr',)
    search_fields = ('campaign__name',)


@admin.register(BannerTemplate)
class BannerTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'width', 'height', 'created_at')
    list_filter = ('template_type', 'created_at')
    search_fields = ('name', 'html_template')

@admin.register(GameData)
class GameDataAdmin(admin.ModelAdmin):
    list_display = ('game_name', 'player_name', 'score', 'level', 'game_type', 'imported_at')
    list_filter = ('game_type', 'imported_at')
    search_fields = ('game_name', 'player_name')

@admin.register(GeneratedBanner)
class GeneratedBannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'game_data', 'created_at')
    list_filter = ('created_at', 'template')
    search_fields = ('name', 'html_content')
    readonly_fields = ('created_at', 'preview_url')