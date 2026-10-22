from django.db import models
from django.conf import settings


class Course(models.Model):

    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    ]

    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    category = models.CharField(
        max_length=100
    )

    thumbnail = models.ImageField(
        upload_to='course_thumbnails/',
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='BEGINNER'
    )

    what_you_learn = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class CourseSection(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    title = models.CharField(
        max_length=200
    )

    content = models.TextField(
        blank=True
    )

    video = models.FileField(
        upload_to='course_videos/',
        blank=True,
        null=True
    )

    notes_pdf = models.FileField(
        upload_to='course_notes/',
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order', 'id']


class Quiz(models.Model):

    section = models.OneToOneField(
        CourseSection,
        on_delete=models.CASCADE,
        related_name='quiz',
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question = models.TextField()

    marks = models.PositiveIntegerField(
        default=1
    )

    order = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return self.question[:50]

    class Meta:
        ordering = ['order', 'id']


class QuizOption(models.Model):

    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name='options'
    )

    option_text = models.CharField(
        max_length=500
    )

    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.option_text


class CourseEnrollment(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_enrollments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_course_enrollment'
            )
        ]

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"


class StudentSectionProgress(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='section_progress'
    )

    section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )

    completed = models.BooleanField(
        default=False
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'section'],
                name='unique_student_section_progress'
            )
        ]

    def __str__(self):
        return f"{self.student.email} - {self.section.title}"


class QuizAttempt(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_quiz_attempts'
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    score = models.PositiveIntegerField(
        default=0
    )

    total_marks = models.PositiveIntegerField(
        default=0
    )

    attempted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.email} - "
            f"{self.quiz.title} - "
            f"{self.score}/{self.total_marks}"
        )




class CoursePayment(models.Model):

    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_payments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        unique=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='CREATED'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.email} - "
            f"{self.course.title} - "
            f"{self.status}"
        )
