from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from cust_auth.models import InstituteRecord, InstituteBranch,InstituteFees,Userone

# Register your models here.

class InstituteRecordAdmin(admin.ModelAdmin):

    list_display = ['name', 'email','mobile','is_active']
    search_fields = ['name', 'email']

class InstituteBranchAdmin(admin.ModelAdmin):

    list_display = ['institute_name','name','mobile','is_active']
    search_fields = ['name', 'email']

class InstituteFeesAdmin(admin.ModelAdmin):

	list_display =['fees_type','amount','is_active']
	search_fields = ['fees_type','amount','is_active']

# class StudentProfileAdmin(admin.ModelAdmin):

# 	list_display = ['first_name','last_name','email','enrollment','mobile','dob','gender','branch','course','address','is_active']
# 	search_fields = ['username','email','is_active']

admin.site.register(InstituteRecord, InstituteRecordAdmin)
admin.site.register(InstituteBranch, InstituteBranchAdmin)
admin.site.register(InstituteFees,InstituteFeesAdmin)
admin.site.register(Userone)