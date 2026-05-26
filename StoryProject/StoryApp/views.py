from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from transformers import pipeline
from googletrans import Translator
from gtts import gTTS
import os

from .models import Story

generator = pipeline('text-generation', model='gpt2')
translator = Translator()

def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def register_action(request):
    if request.method == 'POST':
        username = request.POST['t1']
        email = request.POST['t2']
        password = request.POST['t3']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'data': 'User exists'})

        User.objects.create_user(username=username, email=email, password=password)
        return render(request, 'login.html', {'data': 'Registered Successfully'})


def login_user(request):
    return render(request, 'login.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST['t1']
        password = request.POST['t2']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('generate')
        else:
            return render(request, 'login.html', {'data': 'Invalid Login'})


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
def generate(request):
    if request.method == 'POST':
        prompt = request.POST['prompt']
        language = request.POST['language']

        story = generator(prompt, max_length=300)[0]['generated_text']

        if language != 'en':
            story = translator.translate(story, dest=language).text

        Story.objects.create(
            user=request.user,
            prompt=prompt,
            generated_text=story,
            language=language
        )

        if not os.path.exists('static'):
            os.makedirs('static')

        tts = gTTS(text=story, lang='en')
        tts.save("static/story.mp3")

        return render(request, 'output.html', {'story': story})

    return render(request, 'generate.html')