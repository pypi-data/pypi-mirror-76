from django.contrib.admin import ModelAdmin


class ShortenerModelAdmin(ModelAdmin):
    list_display  = ["url", "pk", "slug", "author", "status"]
    list_filter   = ["created_at", "updated_at"]
    search_fields = ["url", "slug", "status"]
    fieldsets     = (
        ("SEO Information (Optional)", {
            "classes": ["collapse", "wide", "extrapretty"],
            "fields" : ["title", "description", "image"]
        }),
        ("User Data", {
            "classes": ["wide", "extrapretty"],
            "fields" : ["url", "slug"]
        }),
        ("Status", {
            "classes": ["wide", "extrapretty", "collapse"],
            "fields" : ["author", "status"]
        }),
    )