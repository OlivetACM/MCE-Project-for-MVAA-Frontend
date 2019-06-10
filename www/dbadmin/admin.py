from django.contrib import admin
from dbadmin.models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ("CourseID", "CourseNumber", "CourseDescription", "CourseCredit", "CourseEquivalenceNonOC", "InstitutionID", "ReviewerID")
    search_fields = ("CourseNumber",)

admin.site.register(Course, CourseAdmin)

# Register your models here.
