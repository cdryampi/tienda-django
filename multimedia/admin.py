from django.contrib import admin
from multimedia.models import MediaFile, DocumentFile

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at', 'owner')
    search_fields = ('title', 'owner__username')
    list_filter = ('uploaded_at',)

@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)
