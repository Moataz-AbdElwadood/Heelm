from django.contrib import admin
from django.utils.html import format_html
from tafseer.models import Blog

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # Display title, image, and content in the list view
    list_display = ('blog_title', 'image_tag', 'short_description', 'created_at')

    # Make title, content, and image fields searchable
    search_fields = ('blog_title', 'content')

    # Optionally display filters based on creation date
    list_filter = ('created_at',)

    # Display the full form for adding/editing blogs
    fields = ['blog_title', 'content', 'image']

    # Custom method to display the image in the list view as a thumbnail
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = 'Image'

    # Custom method to show a short version of content
    def short_description(self, obj):
        return obj.content[:50]  # Show the first 50 characters
    short_description.short_description = 'Description'
