from django.shortcuts import render, HttpResponse
from .models import Article, Category
from django.core.paginator import Paginator

# Create your views here.


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
    context = {
        "article": article
    }
    return render(request, 'web_site/article_detail.html', context)


def login_view(request):
    return render(request, "web_site/login.html")


def registration_view(request):
    return render(request, "web_site/registration.html")
