from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from .models import Task, Priority, Category, Tag, Comment, Attachment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class PriorityResource(resources.ModelResource):
    class Meta:
        model = Priority

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class TagResource(resources.ModelResource):
    class Meta:
        model = Tag

class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment

class AttachmentResource(resources.ModelResource):
    class Meta:
        model = Attachment

class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        export_order = ('id', 'title', 'user', 'status', 'is_completed', 'due_date', 'priority', 'category', 'tags') 
 
class TaskAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'is_completed', 'due_date', 'priority', 'category')
    list_filter = ('status', 'priority', 'category', 'due_date')
    search_fields = ('title', 'description')
    list_display_links = ('title',)  
    date_hierarchy = 'due_date'
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'is_completed')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'user', 'priority', 'category')
        }),
        ('Dates and Status', {
            'fields': ('due_date', 'status', 'is_completed'),
            'classes': ('collapse',)
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )

    inlines = [CommentInline, AttachmentInline]

    resource_class = TaskResource
    
class PriorityAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PriorityResource
    list_display = ('id', 'level', 'color')

class CategoryAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CategoryResource
    list_display = ('id', 'name', 'color')

class TagAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TagResource
    list_display = ('id', 'name', 'color')

class CommentAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CommentResource
    list_display = ('id', 'text', 'task', 'user', 'created_at')

class AttachmentAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AttachmentResource
    list_display = ('id', 'task', 'file')

admin.site.register(Task, TaskAdmin)
admin.site.register(Priority, PriorityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Attachment, AttachmentAdmin)
