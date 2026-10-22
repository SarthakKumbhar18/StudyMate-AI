from django.contrib import admin
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'description',
        'created_at'
    )

    search_fields = (
        'name',
        'description'
    )

    ordering = (
        'name',
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'course',
        'order'
    )

    list_filter = (
        'course',
    )

    search_fields = (
        'name',
        'course__name'
    )

    ordering = (
        'course',
        'order',
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'topic',
        'get_course',
        'language',
        'difficulty',
        'order',
        'created_at'
    )

    list_filter = (
        'language',
        'difficulty',
        'topic__course',
        'topic'
    )

    search_fields = (
        'title',
        'description',
        'topic__name',
        'topic__course__name'
    )

    ordering = (
        'topic',
        'order'
    )

    def get_course(self, obj):
        return obj.topic.course.name

    get_course.short_description = 'Course'


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):

    list_display = (
        'question',
        'order',
        'is_sample'
    )

    list_filter = (
        'is_sample',
    )

    search_fields = (
        'question__title',
    )

    ordering = (
        'question',
        'order',
    )


@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'question',
        'language',
        'status',
        'attempts',
        'solved',
        'last_attempted_at'
    )

    list_filter = (
        'language',
        'status',
        'solved',
    )

    search_fields = (
        'student__email',
        'question__title',
    )

    ordering = (
        '-last_attempted_at',
    )

    readonly_fields = (
        'last_attempted_at',
    )