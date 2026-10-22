from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'Home/home.html')




def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            full_name = form.cleaned_data['full_name']
            name_parts = full_name.split()

            user.first_name = name_parts[0]

            if len(name_parts) > 1:
                user.last_name = ' '.join(name_parts[1:])

            user.email = form.cleaned_data['email']

            user.save()

            role = form.cleaned_data['role']

            UserRole.objects.create(
                user=user,
                role=role
            )

            if role == 'STUDENT':
                StudentProfile.objects.create(user=user)

            elif role == 'TUTOR':
                TutorProfile.objects.create(user=user)

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'Home/register.html', {'form': form})




def user_login(request):

    if request.method == 'POST':

        selected_role = request.POST.get('role')

        form = LoginForm(
            request,
            data=request.POST
        )

        if not selected_role:
            form.add_error(
                None,
                'Please select Student or Tutor.'
            )

        elif selected_role not in ['student', 'tutor']:
            form.add_error(
                None,
                'Invalid role selected.'
            )

        if form.is_valid():

            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                email=email,
                password=password
            )

            if user is not None:

                roles = list(
                    user.roles.values_list(
                        'role',
                        flat=True
                    )
                )

                selected_role_name = selected_role.upper()

                if selected_role_name not in roles:

                    form.add_error(
                        None,
                        f'You are not registered as a {selected_role.title()}.'
                    )

                else:

                    login(request, user)

                    if selected_role == 'student':
                        return redirect('student_dashboard')

                    elif selected_role == 'tutor':
                        return redirect('tutor_dashboard')

    else:

        form = LoginForm()

    return render(
        request,
        'Home/login.html',
        {
            'form': form
        }
    )




@login_required
def student_dashboard(request):
    
    roles = request.user.roles.values_list('role', flat=True)

    if 'STUDENT' not in roles:
        return render(request, 'Home/home.html')

    return render(request,'Home/student_dashboard.html',{'roles': roles})




@login_required
def tutor_dashboard(request):

    roles = request.user.roles.values_list('role', flat=True)

    if 'TUTOR' not in roles:
        return render(request, 'Home/home.html')

    return render(request,'Home/tutor_dashboard.html',{'roles': roles})



@login_required
def become_tutor(request):

    if not request.user.roles.filter(role='TUTOR').exists():

        UserRole.objects.create(
            user=request.user,
            role='TUTOR'
        )

        TutorProfile.objects.create(
            user=request.user
        )

    return redirect('student_dashboard')


@login_required
def become_student(request):

    if not request.user.roles.filter(role='STUDENT').exists():

        UserRole.objects.create(
            user=request.user,
            role='STUDENT'
        )

        StudentProfile.objects.create(
            user=request.user
        )

    return redirect('tutor_dashboard')



@login_required
def student_profile(request):

    roles = request.user.roles.values_list('role', flat=True)

    if 'STUDENT' not in roles:
        return render(request, 'Home/home.html')

    profile = request.user.student_profile

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('student_profile')

    else:
        form = StudentProfileForm(instance=profile)

    return render(
        request,
        'Home/student_profile.html',
        {
            'form': form,
            'profile': profile
        }
    )


def user_logout(request):
    logout(request)
    return redirect('login')