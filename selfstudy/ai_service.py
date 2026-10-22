from groq import Groq
from django.conf import settings
import json

from .embedding import create_query_embedding
from .vector_store import search_chunks


def get_groq_response(prompt):

    client = Groq(
        api_key=settings.GROQ_API_KEY
    )

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=4000
        )

        return response.choices[0].message.content

    except Exception as e:

        print("GROQ ERROR:")
        print(type(e).__name__)
        print(str(e))

        return None


def generate_explanation(topic):

    prompt = f"""
You are an AI tutor for college students.

Explain the following topic in simple and easy-to-understand language.

Topic:
{topic}

Follow these rules:
- Start with a simple definition.
- Explain the concept step by step.
- Use headings where useful.
- Give simple examples.
- Mention important points.
- Avoid unnecessarily difficult language.
- Make the explanation useful for exam preparation.
"""

    return get_groq_response(prompt)


def generate_summary(topic):

    prompt = f"""
You are an AI tutor for college students.

Create a short and useful summary of the following topic.

Topic:
{topic}

Follow these rules:
- Include only the most important information.
- Use simple language.
- Use bullet points and headings where useful.
- Keep the summary concise.
- Include important definitions, concepts and points.
- Make it useful for quick revision and exam preparation.
- Do not add unnecessary information.
"""

    return get_groq_response(prompt)


def generate_notes(topic):

    prompt = f"""
You are an AI tutor for college students.

Create detailed and well-structured study notes for the following topic.

Topic:
{topic}

Follow these rules:
- Use clear headings and subheadings.
- Start with important definitions.
- Explain important concepts in simple language.
- Use bullet points where appropriate.
- Include important formulas, rules, steps or classifications if relevant.
- Include simple examples where useful.
- Highlight important exam points.
- Keep the notes organized and easy to revise.
- Do not add unnecessary information.
"""

    return get_groq_response(prompt)


def answer_question(topic, question):

    prompt = f"""
You are an AI tutor for college students.

The student is studying the following topic:

Topic:
{topic}

The student has asked this question:

Question:
{question}

Answer the student's question clearly and accurately.

Follow these rules:
- Answer based on the given topic.
- Use simple and easy-to-understand language.
- Explain step by step when necessary.
- Give examples where useful.
- Use headings or bullet points where useful.
- Keep the answer focused on the student's question.
- Make the answer useful for learning and exam preparation.
"""

    return get_groq_response(prompt)


def generate_mcqs(topic):

    prompt = f"""
You are an AI tutor for college students.

Generate exactly 20 multiple-choice questions about this topic:

{topic}

Difficulty distribution:
- 5 simple questions
- 3 intermediate questions
- 2 hard questions

Each question must have exactly 4 options.

Return ONLY valid JSON.

Use this exact structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "difficulty": "simple"
        }}
    ]
}}

Rules:
- Exactly 10 questions.
- Questions 1-5 must be simple.
- Questions 6-8 must be intermediate.
- Questions 9-10 must be hard.
- correct_answer must be only A, B, C or D.
- difficulty must be simple, intermediate or hard.
- Only one option must be correct.
- Do not include explanations.
- Do not use markdown.
- Return only JSON.
"""

    response = get_groq_response(prompt)

    if response is None:
        return None

    response = response.strip()

    if response.startswith("```"):

        response = response.replace(
            "```json",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        response = response.strip()

    try:

        data = json.loads(response)

    except json.JSONDecodeError:

        print("MCQ JSON ERROR")
        print(response)

        return None

    if "questions" not in data:

        print("MCQ QUESTIONS KEY MISSING")
        print(data)

        return None

    if len(data["questions"]) != 10:

        print("MCQ COUNT:", len(data["questions"]))
        print(data)

        return None

    return data["questions"]


def get_material_context(
    topic,
    student_id,
    study_id
):

    query = topic.strip()

    if query == "":
        query = "study material"

    query_embedding = create_query_embedding(
        query
    )

    if query_embedding is None:
        return None

    relevant_chunks = search_chunks(
        query_embedding,
        student_id,
        study_id
    )

    if not relevant_chunks:
        return None

    context = "\n\n".join(
        relevant_chunks
    )

    return context


def answer_question_from_material(
    question,
    student_id,
    study_id
):

    context = get_material_context(
        question,
        student_id,
        study_id
    )

    if context is None:
        return None

    prompt = f"""
You are an AI tutor for college students.

Answer the student's question using the study material provided below.

Study Material:
{context}

Student Question:
{question}

Follow these rules:
- Answer using the provided study material.
- Keep the answer clear and easy to understand.
- Explain step by step when necessary.
- Use examples only when they are supported by the study material.
- Do not make up information.
- If the answer is not available in the study material, clearly say that the information is not available in the uploaded material.
"""

    return get_groq_response(
        prompt
    )


def generate_explanation_from_material(
    topic,
    student_id,
    study_id
):

    context = get_material_context(
        topic,
        student_id,
        study_id
    )

    if context is None:
        return None

    prompt = f"""
You are an AI tutor for college students.

Explain the following topic using the uploaded study material.

Topic:
{topic}

Study Material:
{context}

Follow these rules:
- Use the study material as the primary source.
- Start with a simple definition.
- Explain the concept step by step.
- Use headings where useful.
- Give examples only when supported by the study material.
- Mention important points from the material.
- Use simple language.
- Make the explanation useful for exam preparation.
- Do not make up information that is not supported by the study material.
- If the topic is not covered in the uploaded material, clearly say that the topic is not available in the uploaded material.
"""

    return get_groq_response(
        prompt
    )


def generate_summary_from_material(
    topic,
    student_id,
    study_id
):

    context = get_material_context(
        topic,
        student_id,
        study_id
    )

    if context is None:
        return None

    prompt = f"""
You are an AI tutor for college students.

Create a short and useful summary of the following topic using the uploaded study material.

Topic:
{topic}

Study Material:
{context}

Follow these rules:
- Use the study material as the primary source.
- Include only the most important information.
- Use simple language.
- Use bullet points and headings where useful.
- Keep the summary concise.
- Include important definitions, concepts and points from the material.
- Make it useful for quick revision and exam preparation.
- Do not make up information that is not supported by the study material.
- If the topic is not covered in the uploaded material, clearly say that the topic is not available in the uploaded material.
"""

    return get_groq_response(
        prompt
    )


def generate_notes_from_material(
    topic,
    student_id,
    study_id
):

    context = get_material_context(
        topic,
        student_id,
        study_id
    )

    if context is None:
        return None

    prompt = f"""
You are an AI tutor for college students.

Create detailed and well-structured study notes for the following topic using the uploaded study material.

Topic:
{topic}

Study Material:
{context}

Follow these rules:
- Use the study material as the primary source.
- Use clear headings and subheadings.
- Start with important definitions.
- Explain important concepts in simple language.
- Use bullet points where appropriate.
- Include important formulas, rules, steps or classifications if they are present in the study material.
- Include examples only when supported by the study material.
- Highlight important exam points from the material.
- Keep the notes organized and easy to revise.
- Do not make up information that is not supported by the study material.
- If the topic is not covered in the uploaded material, clearly say that the topic is not available in the uploaded material.
"""

    return get_groq_response(
        prompt
    )


def generate_mcqs_from_material(
    topic,
    student_id,
    study_id
):

    context = get_material_context(
        topic,
        student_id,
        study_id
    )

    if context is None:
        return None

    prompt = f"""
You are an AI tutor for college students.

Generate exactly 10 multiple-choice questions using ONLY the study material provided below.

Topic:
{topic}

Study Material:
{context}

Difficulty distribution:
- Questions 1 to 5: simple
- Questions 6 to 8: intermediate
- Questions 9 to 10: hard

Return ONLY valid JSON.

The response must begin with {{
and end with }}.

Use this exact structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "difficulty": "simple"
        }}
    ]
}}

Rules:
- Exactly 10 questions.
- Exactly 4 options for every question.
- Only one option can be correct.
- correct_answer must be A, B, C or D.
- Questions 1-5 must have difficulty "simple".
- Questions 6-8 must have difficulty "intermediate".
- Questions 9-10 must have difficulty "hard".
- Every question must be based ONLY on the provided study material.
- Do not use outside knowledge.
- Do not invent information.
- Do not include explanations.
- Do not include markdown.
- Do not include any text before or after the JSON.
"""

    response = get_groq_response(
        prompt
    )

    if response is None:
        return None

    response = response.strip()

    if response.startswith("```"):

        response = response.replace(
            "```json",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        response = response.strip()

    try:

        data = json.loads(response)

    except json.JSONDecodeError:

        print("MCQ JSON ERROR")
        print(response)

        return None

    if "questions" not in data:

        print("MCQ QUESTIONS KEY MISSING")
        print(data)

        return None

    if len(data["questions"]) != 10:

        print("MCQ COUNT:", len(data["questions"]))
        print(data)

        return None

    return data["questions"]