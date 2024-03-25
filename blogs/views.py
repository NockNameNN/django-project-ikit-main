from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from .forms import CommentForm, PostFilterForm, PostForm
# from django.shortcuts import render

from .models import Post, Comment


# def page_not_found_view(request, exception):
#     return render(request, '404.html', status=404)

def page_not_found_view(request, exception):
    return render(request, '404.html', {})
class BlogListView(ListView):
    model = Post
    paginate_by = 2
    template_name = "post/post_list.html"
    context_object_name = 'filtered_posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | queryset.filter(description__icontains=search_query)
        if category:
            queryset = queryset.filter(category=category)
        if tag:
            queryset = queryset.filter(tags=tag)

        if not category and not tag and not search_query:
            queryset = Post.objects.all()

        if 'reset' in self.request.GET:
            return Post.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostFilterForm(self.request.GET)
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comment_set.all()
        context['comment_form'] = CommentForm()
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class BlogCreateView(SuccessMessageMixin,  LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post/post_new.html"
    success_message = "%(name)s успешно создан"

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "Пост с таким названием уже существует!")
            return HttpResponseRedirect(reverse("post_new"))


class BlogUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post/post_edit.html"
    success_message = "%(name)s успешно обновлен"

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "Пост с таким названием уже существует!")
            return HttpResponseRedirect(reverse("post_new"))


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    success_url = reverse_lazy("post_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        form.save()


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    category = comment.post.category.slug
    slug = comment.post.slug
    if request.user == comment.author:
        comment.delete()
        messages.success(request, 'Комментарий успешно удален.')
    else:
        messages.error(request, 'У вас нет прав на удаление этого комментария.')
    return HttpResponseRedirect(reverse('post_detail', kwargs={'category': category, 'slug': slug}))
