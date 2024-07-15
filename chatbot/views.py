import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth, messages
from openai import OpenAI
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import Chat
from django.utils import timezone


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def ask_openai(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f'Answer this text: {message}',
            }
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    answer = response.choices[0].message.content
    return answer


@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message,
                    response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('chatbot')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('chatbot')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You Have Been Logged Out')
    return redirect('login')
