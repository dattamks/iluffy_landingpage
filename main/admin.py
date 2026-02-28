from django.contrib import admin
from .models import Plan, PlanFeature, Testimonial, ContactSubmission, ContactInfo


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["name", "monthly_price", "annual_price", "is_popular", "order"]
    list_editable = ["order", "is_popular"]
    inlines = [PlanFeatureInline]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "rating", "is_active", "order"]
    list_editable = ["is_active", "order"]
    list_filter = ["is_active", "rating"]


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ["subject", "email", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    readonly_fields = ["name", "email", "subject", "message", "created_at"]


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    # Singleton — hide add/delete
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
