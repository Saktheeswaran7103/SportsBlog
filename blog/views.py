from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Post, Category
from .forms import PostForm, CommentForm


# =========================
# POST LIST (ONLY USER POSTS)
# =========================
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        # Superuser can see all posts
        if self.request.user.is_superuser:
            return Post.objects.filter(published=True)

        # Normal user sees ONLY their posts
        return Post.objects.filter(
            author=self.request.user,
            published=True
        )


# =========================
# POSTS BY CATEGORY
# =========================
class PostListByCategory(PostListView):
    def get_queryset(self):
        category_name = self.kwargs.get("name")

        if self.request.user.is_superuser:
            return Post.objects.filter(
                category__name__iexact=category_name,
                published=True
            )

        return Post.objects.filter(
            author=self.request.user,
            category__name__iexact=category_name,
            published=True
        )


# =========================
# POST DETAIL
# =========================
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_superuser:
            return queryset

        # Prevent viewing other users' posts
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = self.object
            comment.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        return self.render_to_response(
            self.get_context_data(comment_form=form)
        )


# =========================
# CREATE POST
# =========================
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





# =========================
# SIGNUP VIEW
# =========================
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blog:post_list")
    else:
        form = UserCreationForm()

    return render(
        request,
        "blog/registration/signup.html",
        {"form": form},
    )
