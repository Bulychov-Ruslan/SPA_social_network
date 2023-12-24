# post/api.py
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend, Repost, PostAttachment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer, RepostSerializer


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    reposts = Repost.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    reposts_serializer = RepostSerializer(reposts, many=True)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    else:
        can_send_friendship_request = True

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False
    else:
        can_send_friendship_request = True


    return JsonResponse({
        'posts': posts_serializer.data,
        'reposts': reposts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)


# @api_view(['POST'])
# def post_create(request):
#     form = PostForm(request.POST)
#     attachment = None
#     attachment_form = AttachmentForm(request.POST, request.FILES)

#     if attachment_form.is_valid():
#         attachment = attachment_form.save(commit=False)
#         attachment.created_by = request.user
#         attachment.save()

#     if form.is_valid():
#         post = form.save(commit=False)
#         post.created_by = request.user
#         post.save()

#         if attachment:
#             post.attachments.add(attachment)

#         user = request.user
#         user.posts_count = user.posts_count + 1
#         user.save()

#         serializer = PostSerializer(post)

#         return JsonResponse(serializer.data, safe=False)
#     else:
#         return JsonResponse({'error': 'add somehting here later!...'})
@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post_attachment = PostAttachment.objects.create(
                file=attachment.file,
                created_by=request.user
            )
            post.attachments.add(post_attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        #CREATE NOTIFICATION
        notification = create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})

@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    #CREATE NOTIFICATION
    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def post_repost(request, pk):
    post = Post.objects.get(pk=pk)

    if post.created_by == request.user:
        return JsonResponse({'message': 'You cannot repost your own post.'}, status=400)

    if not post.reposts.filter(created_by=request.user):
        repost = Repost.objects.create(created_by=request.user, original_post=post)

        post.reposts_count = post.reposts_count + 1
        post.reposts.add(repost)
        post.save()

        #CREATE NOTIFICATION
        notification = create_notification(request, 'post_repost', post_id=post.id)

        return JsonResponse({'message': 'repost created'})
    else:
        return JsonResponse({'message': 'post already reposted'})
    

@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})
    
@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)



