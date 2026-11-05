import requests
from django.conf import settings


def generate_interview_questions(subject, role, difficulty):

    api_key = settings.GROQ_API_KEY

    if not api_key:
        return "Groq API key not found. Please check your .env file."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are an expert technical interview coach.

    Generate 5 unique technical interview questions.

    Subject: {subject}
    Job Role: {role}
    Difficulty: {difficulty}

    For each question provide:
    1. Interview question
    2. Correct answer
    3. Simple explanation
    4. One interview tip

    Use simple English.
    Number each question clearly.
    """

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_completion_tokens": 2500
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException:
        return "Unable to connect to Groq. Please check your API key and internet connection."

    except (KeyError, IndexError, ValueError):
        return "Unable to process the AI response. Please try again."
    
def generate_topic_explanation(topic, level):

    api_key = settings.GROQ_API_KEY

    if not api_key:
        return "Groq API key not found. Please check your .env file."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are an expert computer science teacher.

    Explain the following topic to a student.

    Topic: {topic}
    Student Level: {level}

    Follow this structure:

    1. Introduction
    2. Simple Explanation
    3. Important Concepts
    4. Real-world Examples
    5. Advantages and Disadvantages (if applicable)
    6. Short Revision Notes

    Use simple English.
    Explain step by step.
    Include programming examples if relevant.
    """

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_completion_tokens": 2500
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException:
        return "Unable to connect to Groq. Please check your API key and internet connection."

    except (KeyError, IndexError, ValueError):
        return "Unable to process the AI response. Please try again."
