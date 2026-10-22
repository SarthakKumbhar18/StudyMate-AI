from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import *
from .code_executor import *


@login_required
def course_list(request):

    courses = Course.objects.all()

    return render(
        request,
        'Studyplan/courses.html',
        {
            'courses': courses
        }
    )


@login_required
def topic_list(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    topics = course.topics.all()

    return render(
        request,
        'Studyplan/topics.html',
        {
            'course': course,
            'topics': topics
        }
    )


@login_required
def question_list(request, topic_id):

    topic = get_object_or_404(
        Topic,
        id=topic_id
    )

    questions = topic.questions.all()

    return render(
        request,
        'Studyplan/questions.html',
        {
            'topic': topic,
            'questions': questions
        }
    )


@login_required
def question_detail(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id
    )

    test_cases = question.test_cases.filter(
        is_sample=True
    )

    return render(
        request,
        'Studyplan/question_detail.html',
        {
            'question': question,
            'test_cases': test_cases
        }
    )


@login_required
def run_code(request, question_id):

    if request.method != 'POST':
        return JsonResponse(
            {
                'status': 'ERROR',
                'error': 'Invalid request method.'
            },
            status=405
        )

    question = get_object_or_404(
        Question,
        id=question_id
    )

    code = request.POST.get(
        'code',
        ''
    )

    if not code.strip():
        return JsonResponse({
            'status': 'ERROR',
            'error': 'Code cannot be empty.'
        })

    sample_test_case = question.test_cases.filter(
        is_sample=True
    ).first()

    if sample_test_case is None:
        return JsonResponse({
            'status': 'ERROR',
            'error': 'No sample test case is available.'
        })

    # Select executor based on question language

    if question.language == 'PYTHON':

        result = execute_python_code(
            code,
            sample_test_case.input_data
        )

    elif question.language == 'JAVA':

        result = execute_java_code(
            code,
            sample_test_case.input_data
        )

    else:

        return JsonResponse({
            'status': 'ERROR',
            'error': 'Unsupported programming language.'
        })

    return JsonResponse(result)



@login_required
def submit_code(request, question_id):

    if request.method != 'POST':
        return JsonResponse(
            {
                'status': 'ERROR',
                'error': 'Invalid request method.'
            },
            status=405
        )

    question = get_object_or_404(
        Question,
        id=question_id
    )

    code = request.POST.get(
        'code',
        ''
    )

    if not code.strip():
        return JsonResponse({
            'status': 'ERROR',
            'error': 'Code cannot be empty.'
        })

    test_cases = question.test_cases.all()

    if not test_cases.exists():
        return JsonResponse({
            'status': 'ERROR',
            'error': 'No test cases are available.'
        })

    results = []
    final_status = 'ACCEPTED'

    for test_case in test_cases:

        # Select executor based on question language

        if question.language == 'PYTHON':

            result = execute_python_code(
                code,
                test_case.input_data
            )

        elif question.language == 'JAVA':

            result = execute_java_code(
                code,
                test_case.input_data
            )

        else:

            final_status = 'ERROR'

            results.append({
                'test_case': test_case.order,
                'status': 'ERROR',
                'output': '',
                'expected': test_case.expected_output,
                'error': 'Unsupported programming language.'
            })

            break


        # Handle timeout

        if result['status'] == 'TIMEOUT':

            final_status = 'ERROR'

            results.append({
                'test_case': test_case.order,
                'status': 'TIMEOUT',
                'output': '',
                'expected': test_case.expected_output,
                'error': result['error']
            })

            break


        # Handle compilation/runtime error

        if result['status'] == 'ERROR':

            final_status = 'ERROR'

            results.append({
                'test_case': test_case.order,
                'status': 'ERROR',
                'output': result['output'],
                'expected': test_case.expected_output,
                'error': result['error']
            })

            break


        # Compare output

        actual_output = result['output'].strip()

        expected_output = test_case.expected_output.strip()


        if actual_output == expected_output:

            results.append({
                'test_case': test_case.order,
                'status': 'PASSED',
                'output': actual_output,
                'expected': expected_output,
                'error': ''
            })

        else:

            final_status = 'WRONG'

            results.append({
                'test_case': test_case.order,
                'status': 'FAILED',
                'output': actual_output,
                'expected': expected_output,
                'error': ''
            })

            break


    # Save student's attempt

    attempt = QuestionAttempt.objects.filter(
        student=request.user,
        question=question
    ).first()


    if attempt:

        attempt.attempts += 1

        attempt.code = code

        attempt.status = final_status

        attempt.solved = (
            final_status == 'ACCEPTED'
        )

        attempt.language = question.language

        attempt.save()


    else:

        QuestionAttempt.objects.create(
            student=request.user,
            question=question,
            language=question.language,
            code=code,
            status=final_status,
            attempts=1,
            solved=(
                final_status == 'ACCEPTED'
            )
        )


    return JsonResponse({
        'status': final_status,
        'results': results
    })