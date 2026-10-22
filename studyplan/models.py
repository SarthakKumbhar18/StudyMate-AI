from django.db import models
from django.conf import settings


class Course(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Topic(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='topics'
    )

    name = models.CharField(
        max_length=150
    )

    theory = models.TextField(
        blank=True
    )

    order = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.course.name} - {self.name}"

    class Meta:
        ordering = ['order', 'id']


class Question(models.Model):

    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    LANGUAGE_CHOICES = [
        ('PYTHON', 'Python'),
        ('JAVA', 'Java'),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='PYTHON'
    )

    constraints = models.TextField(
        blank=True
    )

    starter_code_python = models.TextField(
        blank=True
    )

    starter_code_java = models.TextField(
        blank=True
    )

    order = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'id']


class TestCase(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='test_cases'
    )

    input_data = models.TextField()

    expected_output = models.TextField()

    is_sample = models.BooleanField(
        default=False
    )

    order = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.question.title} - Test Case {self.order}"

    class Meta:
        ordering = ['order', 'id']


class QuestionAttempt(models.Model):

    STATUS_CHOICES = [
        ('ACCEPTED', 'Accepted'),
        ('WRONG', 'Wrong Answer'),
        ('ERROR', 'Error'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='question_attempts'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    language = models.CharField(
        max_length=10
    )

    code = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    attempts = models.PositiveIntegerField(
        default=1
    )

    solved = models.BooleanField(
        default=False
    )

    last_attempted_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.student.email} - {self.question.title}"