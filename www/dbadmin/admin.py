# from django.contrib import AdminSite
# from django.utils.translation import ugettext_lazy
from django.contrib import admin
from dbadmin.models import Course, Outcome, Reviewer, Institution


# class MyAdminSite(AdminSite):
#     site_title = ugettext_lazy('Olivet MCE Database Administration')
#     site_header = ugettext_lazy('Olivet MCE Administration')
#     index_title = ugettext_lazy('Olivet MCE Database Administration')

class CourseAdmin(admin.ModelAdmin):
    list_display = ("CourseNumber", "CourseName", "CourseDescription", "CourseCredit",
                    "CourseEquivalenceNonOC", "InstitutionID", "ReviewerID")
    search_fields = ("CourseNumber",)


class OutcomeAdmin(admin.ModelAdmin):
    list_display = ("CourseNumber", "OutcomeDescription")
    search_fields = ("CourseNumber",)


class ReviewerAdmin(admin.ModelAdmin):
    list_display = ("ReviewerName", "ReviewerPhone", "ReviewerEmail", "ReviewerDepartment")
    search_fields = ("ReviewerName",)


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("InstitutionName", "InstitutionAddress", "InstitutionCity", "InstitutionState",
                    "InstitutionZipcode", "InstitutionWebSite")
    search_fields = ("InstitutionName",)


# admin_site = MyAdminSite()
admin.site.register(Course, CourseAdmin)
admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(Reviewer, ReviewerAdmin)
admin.site.register(Institution, InstitutionAdmin)


# Register your models here.
