from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Post
from item.models import Category, Item
import openai
from django.conf import settings
from django.http import JsonResponse

def chat_with_gpt(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        openai.api_key = settings.OPENAI_API_KEY

        # Get or initialize the conversation from the session
        conversation = request.session.get('conversation', [])
        
        # Append user's input to the conversation
        conversation.append({"role": "user", "content": user_message})

        # Call the ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Extract the assistant's response from the API response
        system_message = response["choices"][0]["message"]["content"]

        # Append ChatGPT response (assistant role) back to conversation
        conversation.append({"role": "assistant", "content": system_message})

        # Store the updated conversation back to the session
        request.session['conversation'] = conversation
        return JsonResponse({'response': system_message})

    else:
        return JsonResponse({'error': 'Invalid request method'})

def chatbot_view(request):
    return render(request, "chatbot.html")
3
def index(request):
    items = Item.objects.filter(is_sold=True) [0:6]
    categories = Category.objects.all()

    return render(request, "main/index.html", {
        "items": items,
        "categories": categories
    })

def contact(request):
    return render(request, "main/contact.html")

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()

    return render(request, "main/home.html", {"posts": posts})

@login_required(login_url="/login")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # commit=False means don't save to database yet
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, "main/create_post.html", {"form": form})

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})