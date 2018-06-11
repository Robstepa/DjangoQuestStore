from django.contrib.auth.models import User
from django.shortcuts import render


def index(request):
    return render(request, 'index.jinja2')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=name)
            if user.check_password(password):
                return user_page(request, user)
            else:
                return render(request, 'login.jinja2', {'info': 'Wrong password'})
        except User.DoesNotExist:
            return render(request, 'login.jinja2', {'info': 'User does not exist'})
    return render(request, 'login.jinja2')


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        if User.objects.get(email=email):
            return render(request, 'register.jinja2', {'info': 'User already exist'})
        User.objects.create_user(name, email, password)
        return render(request, 'register.jinja2', {'info': 'Done'})
    return render(request, 'register.jinja2')


def user_page(request, user):
    user_id = user.id
    name = user.username
    email = user.email
    if 'session_id' in request.COOKIES:
        session_id = request.COOKIES['session_id']
    response = render(request, 'user_page.jinja2', {'name': name, 'email': email, 'id': user_id})
    response.set_cookie('session_id', user.id)
    return response
