from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, EditForm, CommentForm
from django.conf import settings
from .models import Post, Category
#from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json

def post_list(request):
    posts = Post.objects.filter(approved=True).order_by('-created_at') # Order by created_at descending
    categories = Category.objects.all()
    return render(request, 'news/post_list.html', {
        'posts': posts, 
        'categories': categories
        })

def category_detail(request, category_slug):  # New view for category pages
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, approved=True).order_by('-created_at')
    return render(request, 'news/category_page.html', {'category': category, 'posts': posts})

@login_required
def create_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                # Automatic approval logic (moved to the model's save method)
                post.save()  # This will trigger the save method in the model
                return redirect('post_detail', slug=post.slug)  # Or wherever you want to redirect
        else:
            form = PostForm()  # No initial data needed
        return render(request, 'news/post_create.html', {'form': form})

@login_required
def edit_post(request, slug):  # Add pk parameter to identify the post to edit
    post = get_object_or_404(Post, slug=slug)  # Get the post or 404 if not found
    # Check if the user is the author of the post or a superuser
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_list')  # Or display an error message
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=post) # Use instance=post to populate the form with existing data
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_superuser:
                post.approved = True
            post.save()
            return redirect('post_detail', slug=post.slug)  # Redirect to the updated post detail view
    else:
        form = EditForm(instance=post) # Populate the form with the existing data
    return render(request, 'news/post_form.html', {'form': form, 'post': post}) # Pass the post object to the template

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # Check if the user is the author of the post or a superuser
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_list')  # Or display an error message
    if request.method == 'POST':  # Only handle POST requests for deletion
        post.delete()
        return redirect('post_list')  # Redirect to the home page or wherever you want after deletion
    return render(request, 'news/post_confirm_delete.html', {'post': post})  # Confirmation page

        # @csrf_exempt
        # def like_unlike_post(request, pk):
        #     post = get_object_or_404(Post, pk=pk)

        #     if request.method == 'POST':
        #         try:
        #             data = json.loads(request.body.decode('utf-8'))  # Decode the request body
        #             action = data.get('action')

        #             if not request.user.is_authenticated:
        #                 return HttpResponseForbidden(json.dumps({'error': 'Authentication required'}), content_type='application/json')  # 403 for unauthenticated

        #             if action == 'like':
        #                 post.likes.add(request.user)
        #                 post.unlikes.remove(request.user)  # Ensure only one state
        #             elif action == 'unlike':
        #                 post.unlikes.add(request.user)
        #                 post.likes.remove(request.user)  # Ensure only one state
        #             else:
        #                 return HttpResponseBadRequest(json.dumps({'error': 'Invalid action'}), content_type='application/json')  # 400 for bad action

        #             likes_count = post.likes.count()
        #             unlikes_count = post.unlikes.count()

        #             return JsonResponse({'likes': likes_count, 'unlikes': unlikes_count})

        #         except (json.JSONDecodeError, AttributeError) as e:  # Handle JSON decode and other errors
        #             print(f"Error: {e}")  # Print error for debugging
        #             return HttpResponseBadRequest(json.dumps({'error': 'Invalid request'}), content_type='application/json')  # 400 for bad request

        #     return HttpResponseBadRequest(json.dumps({'error': 'Invalid request method'}), content_type='application/json')  # 400 for bad method

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent=None)  # Get top-level comments (no parent)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.name = request.POST.get('name', 'Anonymous') # Get name from POST data
            parent_id = request.POST.get('parent')
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            return redirect('post_detail', slug=post.slug)  # Redirect to the same post detail page
    else:
        form = CommentForm()
    return render(request, 'news/post_detail.html', {'post': post, 'comments': comments, 'form': form})