from django.contrib import admin
from .models import Category, BlogPost


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author_name", "is_featured", "is_published", "published_at", "views"]
    list_filter = ["is_published", "is_featured", "category"]
    search_fields = ["title", "excerpt", "content", "author_name"]
    list_editable = ["is_published", "is_featured"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at", "views"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "author_name", "author_title", "featured_emoji", "read_time")}),
        ("Content", {"fields": ("excerpt", "content")}),
        ("Publishing", {"fields": ("is_published", "is_featured", "published_at")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("Stats", {"fields": ("views", "created_at", "updated_at")}),
    )
