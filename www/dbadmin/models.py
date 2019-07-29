from django.db import models

# Create your models here.


# Models made from fields in the mce.sqlite3 database
class Course(models.Model):
    #CourseID = models.IntegerField()
    CourseNumber = models.CharField(max_length=128)
    CourseName = models.CharField(max_length=128)
    CourseDescription = models.CharField(max_length=8192)
    CourseCredit = models.CharField(max_length=3)
    CourseEquivalenceNonOC = models.CharField(null=True, blank=True, max_length=128)
    INSTITUTION_CHOICES = (
        (1, "Olivet"),
        (2, "KCC"),
        (3, "Military"),
    )
    InstitutionID = models.IntegerField(
        choices=INSTITUTION_CHOICES,
    )
    ReviewerID = models.IntegerField(null=True, blank=True)

class Outcome(models.Model):
    #OutcomeID = models.IntegerField()
    OutcomeDescription = models.CharField(max_length=1024)
    CourseNumber = models.CharField(max_length=128)


class Reviewer(models.Model):
    #ReviewerID = models.IntegerField()
    ReviewerName = models.CharField(max_length=128)
    ReviewerPhone = models.CharField(max_length=16)
    ReviewerEmail = models.CharField(max_length=128)
    ReviewerDepartment = models.CharField(max_length=8)


class Institution(models.Model):
    #InstitutionID = models.IntegerField()
    InstitutionName = models.CharField(max_length=128)
    InstitutionAddress = models.CharField(max_length=256)
    InstitutionCity = models.CharField(max_length=128)
    InstitutionState = models.CharField(max_length=32)
    InstitutionZipcode = models.CharField(max_length=16)
    InstitutionWebSite = models.CharField(max_length=256)
