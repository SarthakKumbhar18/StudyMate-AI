from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(
            email,
            password,
            **extra_fields
        )


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserRole(models.Model):

    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('TUTOR', 'Tutor')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='roles'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                name='unique_user_role'
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.role}"


class StudentProfile(models.Model):

    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='student_profiles/',
        blank=True,
        null=True
    )

    college = models.CharField(
        max_length=200,
        blank=True
    )

    course = models.CharField(
        max_length=100,
        blank=True
    )

    year = models.CharField(
        max_length=1,
        choices=YEAR_CHOICES,
        blank=True
    )

    education_details = models.TextField(
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    interests = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.user.email} - Student"


class TutorProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tutor_profile'
    )

    def __str__(self):
        return f"{self.user.email} - Tutor"