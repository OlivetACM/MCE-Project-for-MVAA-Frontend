from django.db import models

# Create your models here.


class Course(models.Model):
    CourseID = models.IntegerField()
    CourseNumber = models.CharField(max_length=128)
    CourseName = models.CharField(max_length=128)
    CourseDescription = models.CharField(max_length=8192)
    CourseCredit = models.CharField(max_length=3)
    CourseEquivalenceNonOC = models.CharField(null=True, blank=True, max_length=128)
    INSTITUTION_CHOICES = (
        (1, "Olivet"),
        (2, "KCC"),
        (3, "Military"),
        (0, "Unknown"),
    )
    InstitutionID = models.IntegerField(
        choices=INSTITUTION_CHOICES,
        default=0
    )
    ReviewerID = models.IntegerField(null=True, blank=True)


class Outcome(models.Model):
    OutcomeID = models.IntegerField()
    OutcomeDescription = models.CharField(max_length=1024)
    CourseNumber = models.CharField(max_length=128)


class Reviewer(models.Model):
    ReviewerID = models.IntegerField()
    ReviewerName = models.CharField(max_length=128)
    ReviewerPhone = models.CharField(max_length=16)
    ReviewerEmail = models.CharField(max_length=128)
    ReviewerDepartment = models.CharField(max_length=8)