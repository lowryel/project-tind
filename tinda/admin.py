from django.contrib import admin
from tinda.models import TindaDates, UploadModel, Category, Comment


class TidaDatesAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_of_birth', 'date_joined', 'location')
    list_filter = ('date_of_birth', 'date_joined', 'location')
    search_fields = ('username', 'location')

admin.site.register(TindaDates, TidaDatesAdmin)
admin.site.register(Category)
admin.site.register(UploadModel)
admin.site.register(Comment)

