from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from .models import Article
from django.http import HttpResponseRedirect
from .forms import ArticleForm
# from django.core.paginator import Paginator
# import logging
# logger = logging.getLogger(__name__)

def articles(request):
    # logger.warning("Platform is running at risk")
    articles = Article.objects.all()
    # paginator = Paginator(articles, 2)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    return render(request, 'articles/index.html', {"articles": articles})


def article_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            messages.success(request, "Статья успешно создана!")
            return HttpResponseRedirect(reverse('article.index'))
    else:
        article_form = ArticleForm()
    return render(request, 'articles/create.html', {'article_form': article_form})


def article_update(request, article_id):
    article = Article.objects.get(id=article_id)

    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse('article.update', args=(article_id,)))
    else:
        article_form = ArticleForm(instance=article)
    return render(request, 'articles/update.html', {"article_form": article_form, "article": article})


def article_delete(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        article.delete()
        return HttpResponseRedirect(reverse('article.index'))
    else:
        pass
