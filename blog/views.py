from django.shortcuts import render
from .models import Post, Comment
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

def post_list(request):
    post_list = Post.published.all()

    # Divide 3 pages
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts
    }
    return render(
        request,
        'blog/post/list.html',
        context
    )

def post_detail(request, year, month, day, post):
    # Old version
    '''
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404('No post found')
    '''
    
    post = get_object_or_404(
        Post,  
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }

    return render(
        request,
        'blog/post/detail.html',
        context
    )

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends your read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']}"
            
            send_mail(
                subject,
                message,
                'atabekdemurtaza@gmail.com',
                [cd['to']],   
            )
            sent = True
    
    else:
        form = EmailPostForm()
    
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }

    return render(request, 'blog/post/share.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    
    context = {
        'post': post,
        'comment': comment,
        'form': form
    }

    return render(request, 'blog/post/comment.html', context)
