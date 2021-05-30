from django.contrib import admin
from .models import author,category,article,comment

# Register your models here.
class authorModel(admin.ModelAdmin):
    list_display = ["__str__","id","name"]
    search_fields = ["__str__","detais"]

    class Meta:
        Model=author
admin.site.register(author,authorModel)
class articleModel(admin.ModelAdmin):
    list_display = ["__str__","category","created_at","update_at","image","id","article_author"]
    list_per_page = 10
    search_fields = ["__str__","title"]
    class Meta:
        Model=article
admin.site.register(article,articleModel)

class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    list_per_page = 10
    search_fields = ["__str__","name"]
    class Meta:
        Model=category
admin.site.register(category,categoryModel)

class commentModel(admin.ModelAdmin):
    list_display = ["__str__","name","email","post_comment"]
    search_fields = ["__str__","name"]
    class Meta:
        Model=comment
        
admin.site.register(comment,commentModel)

# class PhotoAdmin(admin.ModelAdmin):
#     search_fields = ('name', 'description', 'keyword', )
# admin.site.register(Photo,PhotoAdmin)
