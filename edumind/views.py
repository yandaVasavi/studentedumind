
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserStudyProfile
from .ai_service import (
    generate_interview_questions,
    generate_topic_explanation
)


# Home page
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'edumind/home.html')


# User Registration
def register_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([first_name, last_name, username, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')

        elif len(password) < 6:
            messages.error(request, 'Password must contain at least 6 characters.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Username already exists.')

        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already registered.')

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            UserStudyProfile.objects.create(user=user)

            login(request, user)

            messages.success(request, 'Account created successfully! Welcome to EduMind.')

            return redirect('dashboard')

    return render(request, 'edumind/register.html')


# User Login
def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')

        else:
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)

                messages.success(request, 'Login successful!')

                return redirect('dashboard')

            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'edumind/login.html')


# User Logout
@login_required
def logout_view(request):

    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')

    return redirect('dashboard')


# User Dashboard
@login_required
def dashboard(request):

    profile, created = UserStudyProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        'profile': profile,
        'user': request.user,
    }

    return render(request, 'edumind/dashboard.html', context)


# AI Interview Preparation
@login_required
def interview_prep(request):

    ai_response = ''
    error_message = ''

    selected_subject = ''
    selected_role = ''
    selected_difficulty = ''

    if request.method == 'POST':

        selected_subject = request.POST.get('subject', '').strip()
        selected_role = request.POST.get('role', '').strip()
        selected_difficulty = request.POST.get('difficulty', '').strip()

        if not all([selected_subject, selected_role, selected_difficulty]):

            error_message = 'Please select subject, job role and difficulty.'

        else:

            ai_response = generate_interview_questions(
                selected_subject,
                selected_role,
                selected_difficulty
            )

    context = {
        'ai_response': ai_response,
        'error_message': error_message,
        'selected_subject': selected_subject,
        'selected_role': selected_role,
        'selected_difficulty': selected_difficulty,
    }

    return render(request, 'edumind/interview_prep.html', context)

# AI Topic Explainer
@login_required
def topic_explainer(request):

    ai_response = ''
    error_message = ''

    selected_topic = ''
    selected_level = ''

    if request.method == 'POST':

        selected_topic = request.POST.get('topic', '').strip()
        selected_level = request.POST.get('level', '').strip()

        if not selected_topic or not selected_level:

            error_message = 'Please enter a topic and select your learning level.'

        else:

            ai_response = generate_topic_explanation(
                selected_topic,
                selected_level
            )

    context = {
        'ai_response': ai_response,
        'error_message': error_message,
        'selected_topic': selected_topic,
        'selected_level': selected_level,
    }

    return render(request, 'edumind/topic_explainer.html', context)

