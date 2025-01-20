from django.contrib import admin
from .models import Task, Priority, Category, Tag, Comment, Attachment

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'is_completed', 'due_date', 'priority', 'category')
    list_filter = ('status', 'priority', 'category', 'due_date')
    search_fields = ('title', 'description')
    list_display_links = ('title',)
    date_hierarchy = 'due_date'
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'is_completed')

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class TaskWithInlinesAdmin(TaskAdmin):
    inlines = [CommentInline, AttachmentInline]

admin.site.register(Task, TaskWithInlinesAdmin)
admin.site.register(Priority)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Attachment)