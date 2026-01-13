from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class ParticipantInline(admin.TabularInline):
    """Inline for displaying participants in Conversation admin"""
    model = Conversation.participants.through
    extra = 1
    verbose_name = "Participant"
    verbose_name_plural = "Participants"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_active=True).order_by('username')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MessageInline(admin.TabularInline):
    """Inline for displaying messages in Conversation admin"""
    model = Message
    extra = 0
    readonly_fields = ['sender', 'timestamp', 'get_preview']
    fields = ['sender', 'get_preview', 'is_read', 'timestamp']
    ordering = ['-timestamp']
    
    def get_preview(self, obj):
        """Show a preview of the message content"""
        preview = obj.content[:50]
        if len(obj.content) > 50:
            preview += "..."
        
        # Add attachment icon if message has attachment
        if obj.attachment:
            preview += f" 📎"
        
        return preview
    get_preview.short_description = "Message Preview"
    
    def has_add_permission(self, request, obj):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'get_participants_list', 
        'is_group', 
        'group_name', 
        'message_count', 
        'last_activity', 
        'created_at'
    ]
    list_filter = [
        'is_group', 
        'created_at', 
        'updated_at'
    ]
    search_fields = [
        'participants__username',
        'participants__email',
        'group_name'
    ]
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'message_count_display',
        'participants_list'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('is_group', 'group_name', 'group_admin')
        }),
        ('Participants', {
            'fields': ('participants_list',)
        }),
        ('Statistics', {
            'fields': ('message_count_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ParticipantInline, MessageInline]
    filter_horizontal = ('participants',)
    autocomplete_fields = ['group_admin']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    def get_participants_list(self, obj):
        """Display participants as clickable links"""
        participants = obj.participants.all()[:5]  # Show first 5 participants
        links = []
        for user in participants:
            url = reverse('admin:auth_user_change', args=[user.id])
            links.append(f'<a href="{url}">{user.username}</a>')
        
        participant_count = obj.participants.count()
        if participant_count > 5:
            links.append(f'<span class="help">+{participant_count - 5} more</span>')
        
        return format_html(', '.join(links))
    get_participants_list.short_description = 'Participants'
    get_participants_list.admin_order_field = 'participants__username'
    
    def participants_list(self, obj):
        """Display all participants in detail view"""
        participants = obj.participants.all()
        return format_html('<br>'.join([f'• {user.username} ({user.email})' for user in participants]))
    participants_list.short_description = 'All Participants'
    
    def message_count(self, obj):
        """Display total message count"""
        return obj.messages.count()
    message_count.short_description = 'Messages'
    
    def message_count_display(self, obj):
        count = obj.messages.count()
        url = reverse('admin:chat_message_changelist') + f'?conversation__id__exact={obj.id}'
        return format_html(f'<a href="{url}">{count} messages</a>')
    message_count_display.short_description = 'Total Messages'
    
    def last_activity(self, obj):
        """Show last message timestamp"""
        last_message = obj.messages.last()
        if last_message:
            return last_message.timestamp
        return obj.updated_at
    last_activity.short_description = 'Last Activity'
    last_activity.admin_order_field = 'updated_at'
    
    def get_queryset(self, request):
        """Optimize queries with select_related and prefetch_related"""
        return super().get_queryset(request).prefetch_related(
            'participants',
            'messages'
        ).select_related('group_admin')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'get_sender', 
        'get_conversation', 
        'content_preview', 
        'has_attachment', 
        'is_read', 
        'timestamp'
    ]
    list_filter = [
        'is_read', 
        'timestamp', 
        'attachment_type',
        'conversation__is_group'
    ]
    search_fields = [
        'content',
        'sender__username',
        'sender__email',
        'conversation__participants__username'
    ]
    readonly_fields = [
        'timestamp',
        'get_attachment_preview',
        'get_conversation_link'
    ]
    fieldsets = (
        ('Message Details', {
            'fields': ('conversation', 'sender', 'content', 'is_read')
        }),
        ('Attachment', {
            'fields': ('attachment', 'attachment_type', 'get_attachment_preview'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('timestamp', 'get_conversation_link'),
            'classes': ('collapse',)
        }),
    )
    raw_id_fields = ['conversation', 'sender']
    autocomplete_fields = ['sender']
    list_select_related = ['sender', 'conversation']
    list_per_page = 50
    date_hierarchy = 'timestamp'
    actions = ['mark_as_read', 'mark_as_unread']
    
    def get_sender(self, obj):
        """Display sender as clickable link"""
        url = reverse('admin:auth_user_change', args=[obj.sender.id])
        return format_html(f'<a href="{url}">{obj.sender.username}</a>')
    get_sender.short_description = 'Sender'
    get_sender.admin_order_field = 'sender__username'
    
    def get_conversation(self, obj):
        """Display conversation as clickable link"""
        url = reverse('admin:chat_conversation_change', args=[obj.conversation.id])
        
        if obj.conversation.is_group and obj.conversation.group_name:
            display_name = obj.conversation.group_name
        else:
            participants = obj.conversation.participants.exclude(id=obj.sender.id)[:3]
            names = [p.username for p in participants]
            if len(names) > 2:
                display_name = f"{', '.join(names[:2])} +{len(names)-2}"
            else:
                display_name = ', '.join(names) if names else "Self"
        
        return format_html(f'<a href="{url}">{display_name}</a>')
    get_conversation.short_description = 'Conversation'
    get_conversation.admin_order_field = 'conversation__id'
    
    def get_conversation_link(self, obj):
        """Display conversation link in detail view"""
        url = reverse('admin:chat_conversation_change', args=[obj.conversation.id])
        return format_html(f'<a href="{url}">View Conversation Details</a>')
    get_conversation_link.short_description = 'Conversation Link'
    
    def content_preview(self, obj):
        """Show truncated content preview"""
        if obj.content:
            preview = obj.content[:80]
            if len(obj.content) > 80:
                preview += "..."
            return preview
        return "-"
    content_preview.short_description = 'Content'
    
    def has_attachment(self, obj):
        """Display attachment status with icon"""
        if obj.attachment:
            file_type = obj.attachment_type or 'file'
            icons = {
                'image': '🖼️',
                'video': '🎥',
                'audio': '🎵',
                'file': '📎'
            }
            icon = icons.get(file_type, '📎')
            return format_html(f'{icon} {file_type.title()}')
        return "-"
    has_attachment.short_description = 'Attachment'
    has_attachment.admin_order_field = 'attachment'
    
    def get_attachment_preview(self, obj):
        """Show attachment preview if it's an image"""
        if obj.attachment and obj.attachment_type == 'image':
            return format_html(
                f'<a href="{obj.attachment.url}" target="_blank">'
                f'<img src="{obj.attachment.url}" style="max-height: 200px; max-width: 200px;" />'
                f'</a>'
            )
        elif obj.attachment:
            return format_html(f'<a href="{obj.attachment.url}" target="_blank">Download File</a>')
        return "No attachment"
    get_attachment_preview.short_description = 'Preview'
    
    def mark_as_read(self, request, queryset):
        """Admin action to mark messages as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        """Admin action to mark messages as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    def get_queryset(self, request):
        """Optimize queries with select_related"""
        return super().get_queryset(request).select_related(
            'sender', 'conversation'
        ).prefetch_related('conversation__participants')


# Optional: Add custom admin site header and title
admin.site.site_header = "PingMe Chat Administration"
admin.site.site_title = "PingMe Admin"
admin.site.index_title = "Welcome to PingMe Chat Admin"