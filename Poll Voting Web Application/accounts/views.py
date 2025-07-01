from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user:
            if role == 'user' and not user.is_staff:
                login(request, user)
                return redirect('poll_list')
            elif role == 'admin' and user.is_staff:
                login(request, user)
                return redirect('admin_poll_list')
            else:
                messages.error(request, f"You are not registered as a {role}.")
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = False  # Not admin
            user.save()
            messages.success(request, 'Signup successful. Please login.')
            return redirect('login')
    return render(request, 'accounts/signup.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required
# @user_passes_test(lambda u: not u.is_staff)
# def user_dashboard(request):
#     return render(request, 'accounts/user_dash.html')

# @login_required
# @user_passes_test(lambda u: u.is_staff)
# def admin_dashboard(request):
#     return render(request, 'accounts/admin_dash.html')
