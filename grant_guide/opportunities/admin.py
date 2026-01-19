"""
Django admin configuration for the opportunities app.
"""
from django.contrib import admin
from django.utils import timezone
from .models import Industry, Province, FundingOpportunity, AuditLog


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_national']
    search_fields = ['name']
    list_filter = ['is_national']
    prepopulated_fields = {'slug': ('name',)}


@admin.action(description='Mark selected as Expired')
def mark_expired(modeladmin, request, queryset):
    queryset.update(status='expired')


@admin.action(description='Mark selected as Needs Review')
def mark_needs_review(modeladmin, request, queryset):
    queryset.update(status='needs_review')


@admin.action(description='Mark selected as Active')
def mark_active(modeladmin, request, queryset):
    queryset.update(status='active')


@admin.action(description='Mark selected as Draft')
def mark_draft(modeladmin, request, queryset):
    queryset.update(status='draft')


@admin.register(FundingOpportunity)
class FundingOpportunityAdmin(admin.ModelAdmin):
    list_display = [
        'funding_name', 'funder', 'funding_type', 'business_stage',
        'deadline', 'status', 'last_verified'
    ]
    list_filter = ['status', 'funding_type', 'business_stage', 'is_rolling', 'industries', 'provinces']
    search_fields = ['funding_name', 'funder', 'description']
    prepopulated_fields = {'slug': ('funding_name',)}
    filter_horizontal = ['industries', 'provinces']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    actions = [mark_expired, mark_needs_review, mark_active, mark_draft]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('funding_name', 'slug', 'funder', 'funding_type', 'description')
        }),
        ('Eligibility', {
            'fields': ('business_stage', 'eligibility_requirements', 'industries', 'provinces')
        }),
        ('Funding Details', {
            'fields': ('funding_amount', 'deadline', 'is_rolling')
        }),
        ('Application', {
            'fields': ('required_documents', 'application_steps', 'apply_link', 'source_link')
        }),
        ('Optional Fields', {
            'fields': ('bbbee_requirement', 'target_groups', 'processing_time', 'contact_email', 'contact_phone'),
            'classes': ('collapse',)
        }),
        ('Status & Verification', {
            'fields': ('status', 'last_verified', 'notes')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Auto-populate last_verified on save
        obj.last_verified = timezone.now().date()
        
        # Track who created/updated
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        
        super().save_model(request, obj, form, change)
        
        # Create audit log
        action = 'updated' if change else 'created'
        AuditLog.objects.create(
            opportunity=obj,
            user=request.user,
            action=action,
            changes={'fields': list(form.changed_data)} if change else {'action': 'created'}
        )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['opportunity', 'user', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['opportunity__funding_name', 'user__username']
    readonly_fields = ['opportunity', 'user', 'action', 'changes', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
