from django.contrib import admin
from  .models import Relation

#admin.site.register(Relation)

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display=('from_user' , 'to_user' , 'created')


# Register your models here.
