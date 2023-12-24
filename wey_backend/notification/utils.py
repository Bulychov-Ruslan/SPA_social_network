
from .models import Notification

from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    created_for = None

    if type_of_notification == 'post_like':
        body = f'{request.user.name} понравился один из ваших постов!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'post_comment':
        body = f'{request.user.name} прокомментировал один из ваших постов!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'post_repost':
        body = f'{request.user.name} сделал репост один из ваших постов!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} отправил запрос в друзья!'

    elif type_of_notification == 'accepted_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_by
        body = f'{request.user.name} принял ваш запрос в друзья!'

    elif type_of_notification == 'rejected_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_by
        body = f'{request.user.name} отклонил ваш запрос в друзья!'
    

    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification, 
        created_by=request.user,
        post_id=post_id,
        created_for=created_for,      
    )

    return notification

