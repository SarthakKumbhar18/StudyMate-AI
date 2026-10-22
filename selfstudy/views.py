from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
from .ai_service import *
from .text_extractor import *
from django.http import JsonResponse

from .chunking import *
from .embedding import *
from .vector_store import *


@login_required
def self_study(request):

    roles = request.user.roles.values_list(
        'role',
        flat=True
    )

    if 'STUDENT' not in roles:

        return render(
            request,
            'Home/home.html'
        )

    if request.method == 'POST':

        topic = request.POST.get(
            'topic',
            ''
        ).strip()

        study_material = request.FILES.get(
            'study_material'
        )

        activities = request.POST.getlist(
            'activities'
        )

        question = request.POST.get(
            'question',
            ''
        ).strip()

        extracted_text = None


        if study_material is not None:

            extracted_text = extract_text(
                study_material
            )

            if extracted_text is None:

                return render(
                    request,
                    'Selfstudy/self_study.html',
                    {
                        'error': 'This file type is not supported yet.'
                    }
                )


        if topic == '' and study_material is None:

            return render(
                request,
                'Selfstudy/self_study.html',
                {
                    'error': 'Please enter a topic or upload study material.'
                }
            )


        if not activities and question == '':

            return render(
                request,
                'Selfstudy/self_study.html',
                {
                    'error': 'Please select an activity or ask a question.'
                }
            )


        explanation = None
        summary = None
        notes = None
        mcqs = None
        ai_error = None
        study = None


        if activities:

            study = SelfStudy.objects.create(
                student=request.user,
                topic=topic,
                study_material=study_material
            )


            if extracted_text:

                chunks = split_text(
                    extracted_text
                )

                embeddings = create_embeddings(
                    chunks
                )

                store_chunks(
                    chunks,
                    embeddings,
                    study.id,
                    request.user.id
                )


            for activity in activities:

                SelfStudyActivity.objects.create(
                    self_study=study,
                    activity=activity
                )


            if 'EXPLAIN' in activities:

                if study_material:

                    explanation = generate_explanation_from_material(
                        topic,
                        request.user.id,
                        study.id
                    )

                else:

                    explanation = generate_explanation(
                        topic
                    )

                if explanation is None:

                    ai_error = 'AI service is temporarily unavailable. Please try again later.'


            if 'SUMMARY' in activities:

                if study_material:

                    summary = generate_summary_from_material(
                        topic,
                        request.user.id,
                        study.id
                    )

                else:

                    summary = generate_summary(
                        topic
                    )

                if summary is None:

                    ai_error = 'AI service is temporarily unavailable. Please try again later.'


            if 'NOTES' in activities:

                if study_material:

                    notes = generate_notes_from_material(
                        topic,
                        request.user.id,
                        study.id
                    )

                else:

                    notes = generate_notes(
                        topic
                    )

                if notes is None:

                    ai_error = 'AI service is temporarily unavailable. Please try again later.'


            if 'MCQS' in activities:

                if study_material:

                    mcqs = generate_mcqs_from_material(
                        topic,
                        request.user.id,
                        study.id
                    )

                else:

                    mcqs = generate_mcqs(
                        topic
                    )

                if mcqs is None:

                    ai_error = 'AI service is temporarily unavailable. Please try again later.'


            return render(
                request,
                'Selfstudy/self_study.html',
                {
                    'success': 'Study request completed successfully.',
                    'topic': topic,
                    'study_id': study.id,
                    'explanation': explanation,
                    'summary': summary,
                    'notes': notes,
                    'mcqs': mcqs,
                    'ai_error': ai_error
                }
            )


        if question != '':

            return render(
                request,
                'Selfstudy/self_study.html',
                {
                    'success': 'Your question has been received.',
                    'topic': topic
                }
            )


    return render(
        request,
        'Selfstudy/self_study.html'
    )


@login_required
def save_mcq_result(request):

    if request.method != 'POST':

        return JsonResponse({
            'success': False
        })

    topic = request.POST.get(
        'topic',
        ''
    ).strip()

    marks = request.POST.get(
        'marks'
    )

    study_id = request.POST.get(
        'study_id'
    )

    if marks is None:

        return JsonResponse({
            'success': False
        })

    try:

        marks = int(marks)

    except ValueError:

        return JsonResponse({
            'success': False
        })

    if study_id:

        try:

            study_id = int(
                study_id
            )

        except ValueError:

            return JsonResponse({
                'success': False
            })

        study = SelfStudy.objects.filter(
            id=study_id,
            student=request.user
        ).first()

        if study is None:

            return JsonResponse({
                'success': False
            })

        if topic == '':

            if study.study_material:

                topic = study.study_material.name

            else:

                topic = 'Self Study'

    elif topic == '':

        return JsonResponse({
            'success': False
        })

    previous_attempts = MCQAttempt.objects.filter(
        student=request.user,
        topic=topic
    ).count()

    attempt_number = previous_attempts + 1

    MCQAttempt.objects.create(
        student=request.user,
        topic=topic,
        attempt_number=attempt_number,
        marks_obtained=marks,
        total_marks=10
    )

    return JsonResponse({
        'success': True,
        'attempt_number': attempt_number
    })


@login_required
def ask_ai(request):

    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'error': 'Invalid request.'
        })


    topic = request.POST.get(
        'topic',
        ''
    ).strip()

    question = request.POST.get(
        'question',
        ''
    ).strip()

    study_id = request.POST.get(
        'study_id'
    )


    if question == '':

        return JsonResponse({
            'success': False,
            'error': 'Please enter a question.'
        })


    if study_id:

        try:

            study_id = int(
                study_id
            )

        except ValueError:

            return JsonResponse({
                'success': False,
                'error': 'Invalid study material.'
            })


        study = SelfStudy.objects.filter(
            id=study_id,
            student=request.user
        ).first()


        if study is None:

            return JsonResponse({
                'success': False,
                'error': 'Study material not found.'
            })


        if study.study_material:

            answer = answer_question_from_material(
                question,
                request.user.id,
                study.id
            )

            if answer is None:

                return JsonResponse({
                    'success': False,
                    'error': 'AI service is temporarily unavailable. Please try again later.'
                })


            return JsonResponse({
                'success': True,
                'answer': answer
            })


    if topic == '':

        return JsonResponse({
            'success': False,
            'error': 'Please enter a topic.'
        })


    answer = answer_question(
        topic,
        question
    )


    if answer is None:

        return JsonResponse({
            'success': False,
            'error': 'AI service is temporarily unavailable. Please try again later.'
        })


    return JsonResponse({
        'success': True,
        'answer': answer
    })