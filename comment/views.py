from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


# Create your views here.


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent if parent.root is None else parent.root
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 发送邮件通知
        comment.send_mail()

        # 返回数据
        data = {'status': 'SUCCESS',
                'username': comment.user.get_nickname_or_username(),
                'comment_time': comment.comment_time.timestamp(),
                'text': comment.text,
                'content_type': ContentType.objects.get_for_model(comment).model
                }
        if parent is not None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = '' if comment.root is None else comment.root.pk
        return JsonResponse(data)
    else:
        data = {'status': 'ERROR',
                'message': list(comment_form.errors.values())[0][0]}
        return JsonResponse(data)
