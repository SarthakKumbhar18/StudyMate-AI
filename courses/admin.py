from django.contrib import admin

from .models import (
    Course,
    CourseSection,
    Quiz,
    QuizQuestion,
    QuizOption,
    CourseEnrollment,
    StudentSectionProgress,
    QuizAttempt,
    CoursePayment
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'tutor',
        'category',
        'price',
        'level',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'level',
        'category'
    )

    search_fields = (
        'title',
        'description',
        'tutor__email'
    )

    ordering = (
        '-created_at',
    )


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'course',
        'order',
        'has_video',
        'has_notes'
    )

    list_filter = (
        'course',
    )

    search_fields = (
        'title',
        'course__title'
    )

    ordering = (
        'course',
        'order'
    )

    def has_video(self, obj):
        return bool(obj.video)

    has_video.boolean = True
    has_video.short_description = 'Video'

    def has_notes(self, obj):
        return bool(obj.notes_pdf)

    has_notes.boolean = True
    has_notes.short_description = 'Notes PDF'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'section'
    )

    search_fields = (
        'title',
        'section__title',
        'section__course__title'
    )


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):

    list_display = (
        'question',
        'quiz',
        'marks',
        'order'
    )

    list_filter = (
        'quiz',
    )

    search_fields = (
        'question',
        'quiz__title'
    )

    ordering = (
        'quiz',
        'order'
    )


@admin.register(QuizOption)
class QuizOptionAdmin(admin.ModelAdmin):

    list_display = (
        'option_text',
        'question',
        'is_correct'
    )

    list_filter = (
        'is_correct',
    )

    search_fields = (
        'option_text',
        'question__question'
    )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'course',
        'enrolled_at'
    )

    list_filter = (
        'course',
    )

    search_fields = (
        'student__email',
        'course__title'
    )

    ordering = (
        '-enrolled_at',
    )


@admin.register(StudentSectionProgress)
class StudentSectionProgressAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'section',
        'completed',
        'completed_at'
    )

    list_filter = (
        'completed',
    )

    search_fields = (
        'student__email',
        'section__title'
    )

    ordering = (
        '-completed_at',
    )


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'quiz',
        'score',
        'total_marks',
        'attempted_at'
    )

    list_filter = (
        'quiz',
    )

    search_fields = (
        'student__email',
        'quiz__title'
    )

    ordering = (
        '-attempted_at',
    )



admin.site.register(CoursePayment)