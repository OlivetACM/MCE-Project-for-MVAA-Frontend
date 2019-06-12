# from django.contrib import AdminSite
# from django.utils.translation import ugettext_lazy
from django.contrib import admin
from dbadmin.models import Course


# class MyAdminSite(AdminSite):
#     site_title = ugettext_lazy('Olivet MCE Database Administration')
#     site_header = ugettext_lazy('Olivet MCE Administration')
#     index_title = ugettext_lazy('Olivet MCE Database Administration')

class CourseAdmin(admin.ModelAdmin):
    list_display = ("CourseID", "CourseNumber", "CourseDescription", "CourseCredit", "CourseEquivalenceNonOC", "InstitutionID", "ReviewerID")
    search_fields = ("CourseNumber",)

# admin_site = MyAdminSite()
admin.site.register(Course, CourseAdmin)


# Register your models here.
