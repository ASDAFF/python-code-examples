from django.contrib import admin
from models import ballotitem, pushitem, image, UserProfile, pushitem_voter, pushimage

class pushitemAdmin(admin.ModelAdmin):
    list_display = ('title','owner','type')
    list_filter = ('type',)
    exclude = ('timestamp','searchfield','voter')

class pushitem_voterAdmin(admin.ModelAdmin):
    list_display = ('pushitem','voted_for','user',)

class pushimageInline(admin.StackedInline):
        model = pushimage
        
class ballotitemAdmin(admin.ModelAdmin):
    list_display = ('name','votes','pushitem')
    inlines = [pushimageInline]

class imageAdmin(admin.ModelAdmin):
    list_display = ('title','caption',)
    class Meta:
        ordering = ['title']

admin.site.register(ballotitem, ballotitemAdmin)
admin.site.register(pushitem, pushitemAdmin)
admin.site.register(image, imageAdmin)
admin.site.register(UserProfile)
admin.site.register(pushitem_voter,pushitem_voterAdmin)