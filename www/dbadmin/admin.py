from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from dbadmin.models import Course, Outcome, Reviewer, Institution




# list_display = what we want shown in the admin site
# search_fields = what we want to search by, seems to do all at once
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

# def equivalency(request):
#     context = dict(
#         admin.site.each_context(request),
#     )
#     return render_to_response(request, 'mce/admin/equivalency.html', context)
#
#

#
class MyAdminSite(AdminSite):

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls += [path('equivalency/', self.admin_view(self.equivalency))]
        return urls

    def equivalency(request):
        context = dict(
            admin.site.each_context(request),
        )
        return render_to_response(request, 'mce/admin/equivalency.html', context)



admin_site = MyAdminSite()

admin.site.register_view('equivalency', urlname='equivalency', name='Generate Equivalency Review', view=admin_site)
