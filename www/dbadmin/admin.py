from django.contrib import admin
from dbadmin.models import Course, Outcome, Reviewer, Institution

from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


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

# Must use login required decorator to restrict usage to admins
@login_required()
def equivalency(request):
    context = dict(
        admin.site.each_context(request),
    )
    return render_to_response(request, 'mce/admin/equivalency.html', context)

# register the view here instead of using a decorator, as we need login_required
admin.site.register_view('equivalency', urlname='equivalency', name='Generate Equivalency Review', view=equivalency)
