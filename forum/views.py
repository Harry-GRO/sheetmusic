from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q
from .models import Post, Comment, Genre
from .forms import PostForm, CommentForm
import os


def post_list(request):
    posts = Post.objects.select_related('author', 'genre').all()
    genres = Genre.objects.all()

    query = request.GET.get('q', '')
    genre_slug = request.GET.get('genre', '')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__username__icontains=query)
        )
    if genre_slug:
        posts = posts.filter(genre__slug=genre_slug)

    return render(request, 'forum/post_list.html', {
        'posts': posts,
        'genres': genres,
        'query': query,
        'active_genre': genre_slug,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author').all()
    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to comment.')
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment posted.')
            return redirect('post_detail', pk=pk)

    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Sheet music posted successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'forum/post_form.html', {'form': form, 'action': 'Upload'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated.')
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/post_form.html', {'form': form, 'action': 'Edit', 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('post_list')
    return render(request, 'forum/post_confirm_delete.html', {'post': post})


def post_download(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.file:
        raise Http404('No file attached to this post.')
    post.download_count += 1
    post.save(update_fields=['download_count'])
    file_path = post.file.path
    if not os.path.exists(file_path):
        raise Http404('File not found.')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post_detail', pk=post_pk)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted.')
    return redirect('post_detail', pk=post_pk)
