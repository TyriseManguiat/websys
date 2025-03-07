from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post, Comment  # ✅ Added Comment model
from .forms import EmailPostForm, CommentForm  # ✅ Added CommentForm

def post_share(request, post_id):
    """Handles sharing a post via email."""
    post = get_object_or_404(Post.published, id=post_id)  # Fixed the manager
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_list(request):
    """Handles listing of all published posts with pagination."""
    object_list = Post.published.all()  # Ensure this gets all published posts
    print(f"Total published posts: {object_list.count()}")  # Debugging

    paginator = Paginator(object_list, 3)  # 3 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    print(f"Current page: {page}, Posts on this page: {len(posts)}")  # Debugging
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, slug):
    """Handles displaying a single post with comments."""
    post = get_object_or_404(Post.published,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # ✅ Added code to handle comments
    comments = post.comments.filter(active=True)  # Fetch only active comments
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })
