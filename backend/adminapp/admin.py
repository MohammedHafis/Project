# from django.contrib import admin

# from django.contrib import admin
# from .models import User, Movie, View_history, Watch_later
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# # Custom User Admin
# class UserAdmin(BaseUserAdmin):
#     list_display = ('id', 'email', 'name', 'is_admin')
#     search_fields = ('email', 'name')
#     ordering = ('email',)
    
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('name',)}),
#         ('Permissions', {'fields': ('is_admin', 'is_superuser')}),
#     )
    
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'name', 'password1', 'password2'),
#         }),
#     )
    
#     filter_horizontal = ()
#     list_filter = ()

# # Movie Admin
# class MovieAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'views')
#     search_fields = ('title',)

# # View History Admin
# class ViewHistoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'movie', 'date')

# # Watch Later Admin
# class WatchLaterAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'movie')

# # Finally register all models
# admin.site.register(User, UserAdmin)
# admin.site.register(Movie, MovieAdmin)
# admin.site.register(View_history, ViewHistoryAdmin)
# admin.site.register(Watch_later, WatchLaterAdmin)

