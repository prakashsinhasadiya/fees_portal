from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib.auth.models import User
from cust_auth.models import InstituteRecord, InstituteBranch,InstituteFees,StudentProfile

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



class StudentProfileAdmin(admin.StackedInline):

    model = StudentProfile
    fk_name = 'user'

class UserAdmin(UserAdmin):

    inlines = [StudentProfileAdmin]
        # list_display = ['enrollment','mobile','dob','gender','branch','course','address','is_active']
    # search_fields = ['username','email','is_active']

admin.site.register(InstituteRecord, InstituteRecordAdmin)
admin.site.register(InstituteBranch, InstituteBranchAdmin)
admin.site.register(InstituteFees,InstituteFeesAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)