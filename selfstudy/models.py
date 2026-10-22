from django.db import models
from accounts.models import User


class SelfStudy(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='self_studies'
    )

    topic = models.CharField(
        max_length=200,
        blank=True
    )

    study_material = models.FileField(
        upload_to='study_materials/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.email} - {self.topic}"


class SelfStudyActivity(models.Model):

    ACTIVITY_CHOICES = [
        ('EXPLAIN', 'Explanation'),
        ('SUMMARY', 'Summary'),
        ('NOTES', 'Generate Notes'),
        ('MCQS', 'Generate MCQs'),
    ]

    self_study = models.ForeignKey(
        SelfStudy,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    activity = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES
    )

    def __str__(self):
        return f"{self.self_study} - {self.activity}"
    
    
    
class MCQAttempt(models.Model):
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mcq_attempts'
    )

    topic = models.CharField(
        max_length=200
    )

    attempt_number = models.PositiveIntegerField()

    marks_obtained = models.PositiveIntegerField()

    total_marks = models.PositiveIntegerField(
        default=20
    )

    attempted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.email} - {self.topic} - Attempt {self.attempt_number}"