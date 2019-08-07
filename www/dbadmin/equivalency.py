from django.contrib import admin
from dbadmin.models import Course, Outcome, Reviewer, Institution

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