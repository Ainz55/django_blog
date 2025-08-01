from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from .models import Article, Category, Comment, ArticleCountView
from django.core.paginator import Paginator

from .forms import LoginForm, RegistrationForm, ArticleForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import DeleteView, UpdateView


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'web_site/article_form.html'
    form_class = ArticleForm
    # success_url = '/'


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'web_site/article_confirm_delete.html'
    success_url = '/'


def home_view(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        "articles": articles
    }
    return render(request, 'web_site/index.html', context)


def category_articles(request, category_id):
    category = Category.objects.get(pk=category_id)
    articles = category.articles.all()
    context = {
        "articles": articles
    }
    return render(request, 'web_site/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)

    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key

    viewed_items = ArticleCountView.objects.filter(
        article=article,
        session_id=session_key
    )

    if viewed_items.count() == 0 and str(session_key) != "None":
        viewed = ArticleCountView()
        viewed.article = article
        viewed.session_id = session_key
        viewed.save()

        article.views += 1
        article.save()

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect('article_detail', article.pk)
    else:
        form = CommentForm()

    comments = article.comment_set.all()


    context = {
        "article": article,
        "form": form,
        "comments": comments
    }
    return render(request, 'web_site/article_detail.html', context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "web_site/login.html", context)


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        "form": form
    }
    return render(request, "web_site/registration.html", context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('article_detail', form.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, "web_site/article_form.html", context)


def profile_view(request, username):
    from datetime import datetime

    user = User.objects.filter(username=username).first()
    now_day = datetime.now().date()
    joined_day = user.date_joined.date()
    total = now_day - joined_day

    articles = Article.objects.filter(author=user)
    total_views = sum([article.views for article in articles])
    total_comments = sum([article.comment_set.all().count() for article in articles])


    context = {
        'user': user,
        'experience': total.days,
        'total_views': total_views,
        'total_comments': total_comments,
        'articles': articles
    }
    return render(request, "web_site/profile.html", context)


def add_like_or_dislike(request, obj_type, obj_id, action):
    from django.shortcuts import get_object_or_404
