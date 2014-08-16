from symbol import argument
from LinkedApp.models import Invitations, Notifications, Connection, Message
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required()
def notifications(request):
    aruments = {}
    aruments['invitations'] = []
    aruments['un_viewed_notifications'] = []
    aruments['connections'] = []
    aruments['connected_users'] = []
    aruments['invited_users'] = []
    aruments['sent_invitations'] = []
    aruments['viewed_notifications'] = []
    aruments['un_viewed_messages'] = []
    aruments['viewed_messages'] = []
    aruments['BASE_URL'] = settings.BASE_URL
    aruments['socket_port'] = settings.SOCKJS_PORT
    aruments['socket_channel'] = settings.SOCKJS_CHANNEL

    try:
        aruments['invitations'] = Invitations.objects.filter(receiver_id=request.user.id)
    except Invitations.DoesNotExist:
        aruments['invitations'] = []

    try:
        aruments['sent_invitations'] = Invitations.objects.filter(sender_id=request.user)
    except Invitations.DoesNotExist:
        aruments['sent_invitations'] = []

    try:
        aruments['un_viewed_notifications'] = Notifications.objects.filter(Q(of_whom=request.user.id) & Q(viewed_status=False))
    except Notifications.DoesNotExist:
        aruments['un_viewed_notifications'] = []

    try:
        aruments['viewed_notifications'] = Notifications.objects.filter(Q(of_whom=request.user.id) & Q(viewed_status=True)).order_by('-id')[:5]
    except Notifications.DoesNotExist:
        aruments['viewed_notifications'] = []

    try:
        aruments['connections'] = Connection.objects.filter(of_whom=request.user)
    except Connection.DoesNotExist:
        aruments['connections'] = []

    for row in aruments['connections']:
        aruments['connected_users'].append(row.with_whom)

    for row in aruments['sent_invitations']:
        aruments['invited_users'].append(row.receiver_id)

    try:
        aruments['un_viewed_messages'] = Message.objects.filter(Q(to=request.user) & Q(viewed_status=False)).order_by('-id')
    except Message.DoesNotExist:
        aruments['un_viewed_messages'] = []

    try:
        aruments['viewed_messages'] = Message.objects.filter(Q(to=request.user)  & Q(viewed_status=True)).order_by('-id')
    except Message.DoesNotExist:
        aruments['viewed_messages'] = []

    try:
        aruments['inbox_messages'] = Message.objects.filter(Q(to=request.user)).order_by('-id')
    except Message.DoesNotExist:
        aruments['inbox_messages'] = []

    try:
        aruments['sent_messages'] = Message.objects.filter(Q(of_whom=request.user)).order_by('-id')
    except Message.DoesNotExist:
        aruments['sent_messages'] = []

    return aruments







