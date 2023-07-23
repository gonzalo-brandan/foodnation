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

        # Call the OpenAI API to get the model's response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=100
        )

        # Extract the generated message from the API response
        chatbot_response = response.choices[0].text.strip()

        # Return the chatbot response as JSON
        return JsonResponse({'response': chatbot_response})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def chatbot_view(request):
    return render(request, "chatbot.html")

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