from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

def login_view(request):
    print("LOGIN ViEW HIT")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')   # 🔥 redirect to homepage
        else:
            return render(request, 'Auth/login.html', {'error': 'Invalid username or password'})

    return render(request, 'Auth/login.html')


def Register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("Form Valid")
            user = form.save()
            # Removed auto-login after registration
            return redirect('login')  # Redirect to login page after successful registration
        else:
            print("Form Errors", form.errors)
            return render(request, 'Auth/Register.html', {'form': form})
    else:
        form = CustomUserCreationForm()

    return render(request, 'Auth/Register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')