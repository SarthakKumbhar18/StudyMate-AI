from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse 
from .models import *


import razorpay

from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import CoursePayment

@login_required
def my_courses(request):

    courses = Course.objects.filter(
        tutor=request.user
    )

    return render(
        request,
        'Courses/my_courses.html',
        {
            'courses': courses
        }
    )


@login_required
def create_course(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        level = request.POST.get('level')
        what_you_learn = request.POST.get('what_you_learn')

        thumbnail = request.FILES.get('thumbnail')

        Course.objects.create(
            tutor=request.user,
            title=title,
            description=description,
            category=category,
            price=price,
            level=level,
            what_you_learn=what_you_learn,
            thumbnail=thumbnail
        )

        return redirect('my_courses')

    return render(
        request,
        'Courses/create_course.html'
    )


@login_required
def manage_course(request, course_id):

    course = Course.objects.get(
        id=course_id,
        tutor=request.user
    )

    sections = course.sections.all()

    return render(
        request,
        'Courses/manage_course.html',
        {
            'course': course,
            'sections': sections
        }
    )


@login_required
def add_section(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        tutor=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title')
        content = request.POST.get('content')
        order = request.POST.get('order')

        video = request.FILES.get('video')
        notes_pdf = request.FILES.get('notes_pdf')

        CourseSection.objects.create(
            course=course,
            title=title,
            content=content,
            video=video,
            notes_pdf=notes_pdf,
            order=order
        )

        return redirect(
            'manage_course',
            course_id=course.id
        )

    return render(
        request,
        'Courses/add_section.html',
        {
            'course': course
        }
    )


@login_required
def edit_section(request, section_id):

    section = get_object_or_404(
        CourseSection,
        id=section_id,
        course__tutor=request.user
    )

    if request.method == 'POST':

        section.title = request.POST.get('title')
        section.content = request.POST.get('content')
        section.order = request.POST.get('order')

        video = request.FILES.get('video')
        notes_pdf = request.FILES.get('notes_pdf')

        if video:
            section.video = video

        if notes_pdf:
            section.notes_pdf = notes_pdf

        section.save()

        return redirect(
            'manage_course',
            course_id=section.course.id
        )

    return render(
        request,
        'Courses/edit_section.html',
        {
            'section': section
        }
    )


@login_required
def delete_section(request, section_id):

    section = get_object_or_404(
        CourseSection,
        id=section_id,
        course__tutor=request.user
    )

    course_id = section.course.id

    if request.method == 'POST':

        section.delete()

        return redirect(
            'manage_course',
            course_id=course_id
        )

    return render(
        request,
        'Courses/delete_section.html',
        {
            'section': section
        }
    )



@login_required
def manage_quiz(request, section_id):

    section = get_object_or_404(
        CourseSection,
        id=section_id,
        course__tutor=request.user
    )

    try:
        quiz = section.quiz
    except Quiz.DoesNotExist:
        quiz = None

    if request.method == 'POST':

        title = request.POST.get('title')

        Quiz.objects.create(
            section=section,
            title=title
        )

        return redirect(
            'manage_quiz',
            section_id=section.id
        )

    return render(
        request,
        'Courses/manage_quiz.html',
        {
            'section': section,
            'quiz': quiz
        }
    )


@login_required
def add_question(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        section__course__tutor=request.user
    )

    if request.method == 'POST':

        question_text = request.POST.get('question')
        marks = request.POST.get('marks')
        correct_option = request.POST.get('correct_option')

        question = QuizQuestion.objects.create(
            quiz=quiz,
            question=question_text,
            marks=marks,
            order=quiz.questions.count() + 1
        )

        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')

        options = [
            ('A', option_a),
            ('B', option_b),
            ('C', option_c),
            ('D', option_d)
        ]

        for option_key, option_text in options:

            QuizOption.objects.create(
                question=question,
                option_text=option_text,
                is_correct=(option_key == correct_option)
            )

        return redirect(
            'manage_quiz',
            section_id=quiz.section.id
        )

    return render(
        request,
        'Courses/add_question.html',
        {
            'quiz': quiz
        }
    )



@login_required
def edit_question(request, question_id):

    question = get_object_or_404(
        QuizQuestion,
        id=question_id,
        quiz__section__course__tutor=request.user
    )

    options = list(
        question.options.all()
    )

    if request.method == 'POST':

        question.question = request.POST.get('question')
        question.marks = request.POST.get('marks')

        question.save()

        option_values = [
        request.POST.get('option_1'),
        request.POST.get('option_2'),
        request.POST.get('option_3'),
        request.POST.get('option_4')
    ]

        correct_option = request.POST.get(
            'correct_option'
        )

        for index, option in enumerate(options):

            option.option_text = option_values[index]

            option.is_correct = (
                index == ord(correct_option) - ord('A')
            )

            option.save()

        return redirect(
            'manage_quiz',
            section_id=question.quiz.section.id
        )

    return render(
        request,
        'Courses/edit_question.html',
        {
            'question': question,
            'options': options
        }
    )



@login_required
def delete_question(request, question_id):

    question = get_object_or_404(
        QuizQuestion,
        id=question_id,
        quiz__section__course__tutor=request.user
    )

    quiz_id = question.quiz.id
    section_id = question.quiz.section.id

    if request.method == 'POST':

        question.delete()

        return redirect(
            'manage_quiz',
            section_id=section_id
        )

    return render(
        request,
        'Courses/delete_question.html',
        {
            'question': question,
            'quiz_id': quiz_id
        }
    )

@login_required
def browse_courses(request):

    courses = Course.objects.filter(
        status='PUBLISHED'
    ).order_by('-created_at')

    return render(
        request,
        'Courses/browse_courses.html',
        {
            'courses': courses
        }
    )


@login_required
def course_detail(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        status='PUBLISHED'
    )

    sections = course.sections.all()

    enrollment = CourseEnrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    return render(
        request,
        'Courses/course_detail.html',
        {
            'course': course,
            'sections': sections,
            'enrollment': enrollment
        }
    )


@login_required
def course_learning(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        status='PUBLISHED'
    )

    # Make sure student is enrolled
    get_object_or_404(
        CourseEnrollment,
        student=request.user,
        course=course
    )

    sections = course.sections.all()

    section_id = request.GET.get('section')

    if section_id:

        current_section = get_object_or_404(
            CourseSection,
            id=section_id,
            course=course
        )

    else:

        current_section = sections.first()


    # --------------------------------
    # QUIZ SUBMISSION
    # --------------------------------

    if request.method == 'POST':

        quiz_id = request.POST.get('quiz_id')

        quiz = get_object_or_404(
            Quiz,
            id=quiz_id,
            section=current_section
        )

        questions = quiz.questions.all()

        score = 0
        total_marks = 0


        for question in questions:

            total_marks += question.marks

            selected_option_id = request.POST.get(
                f'question_{question.id}'
            )

            if selected_option_id:

                selected_option = QuizOption.objects.filter(
                    id=selected_option_id,
                    question=question
                ).first()

                if selected_option and selected_option.is_correct:

                    score += question.marks


        # Save quiz attempt

        QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_marks=total_marks
        )


        # Redirect back to the same section
        # with score information in URL

        return redirect(
            f'/courses/{course.id}/learn/?section={current_section.id}&score={score}&total={total_marks}'
        )


    # --------------------------------
    # QUIZ RESULT
    # --------------------------------

    score = request.GET.get('score')
    total = request.GET.get('total')


    return render(
        request,
        'Courses/course_learning.html',
        {
            'course': course,
            'sections': sections,
            'current_section': current_section,
            'score': score,
            'total': total
        }
    )



razorpay_client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)




@login_required
@require_POST
def create_course_order(request, course_id):

    print("CREATE COURSE ORDER VIEW CALLED")

    course = get_object_or_404(
        Course,
        id=course_id,
        status='PUBLISHED'
    )

    print("COURSE FOUND:", course.title, "PRICE:", course.price)


    # Already enrolled? No payment needed.
    if CourseEnrollment.objects.filter(
        student=request.user,
        course=course
    ).exists():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('course_detail', course_id=course.id)

    # Free courses should not go through paid checkout.
    if course.price <= Decimal('0.00'):
        messages.error(request, 'This course does not require payment.')
        return redirect('course_detail', course_id=course.id)

    # Razorpay accepts amounts in paise.
    amount_paise = int(course.price * 100)

    try:
        order = razorpay_client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f'course_{course.id}_user_{request.user.id}',
        })

        print("RAZORPAY ORDER CREATED:", order.get('id'))

        CoursePayment.objects.create(
            student=request.user,
            course=course,
            razorpay_order_id=order['id'],
            amount=course.price,
            status='CREATED'
        )

    except Exception:
        messages.error(
            request,
            'Unable to start payment. Please try again.'
        )
        return redirect('course_detail', course_id=course.id)


#     return HttpResponse(
#     f"""
#     <h1>Razorpay Order Created Successfully</h1>
#     <p>Course: {course.title}</p>
#     <p>Order ID: {order['id']}</p>
#     <p>Amount: ₹{course.price}</p>
#     """
# )

    return render(
        request,
        'Courses/razorpay_checkout.html',
        {
            'course': course,
            'order_id': order['id'],
            'amount_paise': amount_paise,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'callback_url': request.build_absolute_uri(
                reverse('verify_course_payment')
            ),
            'student_name': request.user.get_full_name(),
            'student_email': request.user.email,
        }
    )




@login_required
@require_POST
def verify_course_payment(request):

    order_id = request.POST.get('razorpay_order_id', '')
    payment_id = request.POST.get('razorpay_payment_id', '')
    signature = request.POST.get('razorpay_signature', '')

    payment_record = get_object_or_404(
        CoursePayment,
        razorpay_order_id=order_id,
        student=request.user
    )

    # Never trust a browser success message alone.
    if payment_record.status == 'PAID':
        return redirect(
            'course_detail',
            course_id=payment_record.course_id
        )

    if not payment_id or not signature:
        messages.error(request, 'Payment verification details are missing.')
        return redirect(
            'course_detail',
            course_id=payment_record.course_id
        )

    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        })

        # Retrieve the payment from Razorpay and check its details.
        payment_details = razorpay_client.payment.fetch(payment_id)

        if payment_details.get('order_id') != order_id:
            raise ValueError('Payment order does not match.')

        if payment_details.get('status') != 'captured':
            messages.warning(
                request,
                'Payment has not been captured yet. Please check its status.'
            )
            return redirect(
                'course_detail',
                course_id=payment_record.course_id
            )

        if int(payment_details.get('amount', 0)) != int(
            payment_record.amount * 100
        ):
            raise ValueError('Payment amount does not match.')

        if payment_details.get('currency') != 'INR':
            raise ValueError('Payment currency does not match.')

        with transaction.atomic():

            locked_payment = CoursePayment.objects.select_for_update().get(
                pk=payment_record.pk
            )

            if locked_payment.status != 'PAID':

                locked_payment.razorpay_payment_id = payment_id
                locked_payment.status = 'PAID'
                locked_payment.save(
                    update_fields=[
                        'razorpay_payment_id',
                        'status'
                    ]
                )

                CourseEnrollment.objects.get_or_create(
                    student=locked_payment.student,
                    course=locked_payment.course
                )

        messages.success(
            request,
            'Payment verified. You are now enrolled!'
        )

        return redirect(
            'course_detail',
            course_id=payment_record.course_id
        )

    except Exception:
        messages.error(
            request,
            'Payment verification failed. If money was deducted, '
            'check the Razorpay dashboard before retrying.'
        )

        return redirect(
            'course_detail',
            course_id=payment_record.course_id
        )
