# -*- coding: utf-8 -*-

from django_socketio import events
from apps.api.sockets.actions import *

ACTIONS = {
    'no_action': no_action,
    'send_text': send_text,
    'track_list': track_list,
    'get_playlist': get_playlist,
    'get_all_playlists': get_all_playlists,
    'get_username': get_username,
    'users_online': users_online,
    'latest_songs': latest_songs,
    'up_vote': up_vote,
    'down_vote': down_vote,
    'latest_votes': latest_votes,
    'was_played': was_played,
    'add_to_playlist': add_to_playlist,
    'create_playlist': create_playlist,
    'users_playlists': users_playlists,
    'follow_playlist': follow_playlist,
    'unfollow_playlist': unfollow_playlist,
    'text_chat_front': messages_chat,
    'new_message_front': update_messages,
    'load_messages_previous': load_message_previous,
    'playing_now': playing_now,
    'new_message_front': update_messages,
    'set_volume': set_volume

}


@events.on_connect()
def connected(request, socket, message):
    print 'CONNECTED'

@events.on_message(channel='^player')
def message(request, socket, context, message):
    ACTIONS.get(message.get('action'), ACTIONS['no_action'])(request, socket, context, message)


@events.on_unsubscribe(channel="^player")
def unsubscribe(request, socket, context, channel):
    print 'On unsubscribe'


@events.on_disconnect(channel="^player")
def disconnect(request, socket, context):
    try:
        red.del_from_users(socket.session.session_id)
        message = {}
        message['send'] = False
        users_online(request, socket, context, message=message)
    except:
        pass


@events.on_finish(channel="^player")
def finish(request, socket, context):
    """
    Event handler for a socket session ending in a room. Broadcast
    the user leaving and delete them from the DB.
    """
    print 'On finish'
    try:
        user = context["user"]
    except KeyError:
        return
