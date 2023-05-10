from django.shortcuts import render
from .forms import RelationsForm
from .functions_postgres import PostgresTools
from .functions_redis import RedisTools

postgre_tool = PostgresTools()
redis_tool = RedisTools()
redis_tool.completion_user()


def for_user(request):
    username = ''
    if request.method == 'POST':
        form = RelationsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user')
    return username


def for_two_users(request):
    user = ''
    user_friend = ''
    if request.method == 'POST':
        form = RelationsForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            user_friend = form.cleaned_data.get('user_friend')
    return user, user_friend


def relations(request):
    username1 = ''
    username2 = ''
    status = ''
    form = RelationsForm(request.POST or None)
    if form.is_valid():
        username1 = form.cleaned_data.get('user')
        username2 = form.cleaned_data.get('user_friend')
        status = form.cleaned_data.get('status')
    form = RelationsForm()
    data = {
        'form': form
    }
    return data, username1, username2, status


def hello(request):
    return render(request, 'user/hello.html')


def create(request):
    username = for_user(request)
    postgre_tool.create_user(username)
    redis_tool.set_user(username)
    form = RelationsForm()
    data = {
        'form': form
    }
    return render(request, 'user/create_user.html', data)


def send(request):
    user1, user2 = for_two_users(request)
    postgre_tool.send_friendship(user1, user2)
    redis_tool.add_relation(user1, user2)
    form = RelationsForm()
    data = {
        'form': form
    }
    return render(request, 'user/send_friend.html', data)


def accept(request):
    data, user1,user2 = for_two_users(request)
    postgre_tool.accept_friendship(user1, user2)
    redis_tool.del_relation(f'{user1}_incoming', user2)
    redis_tool.del_relation(f'{user2}_outgoing', user1)
    #redis_tool.set_relation(f'{user1}_friend', user2)
    #redis_tool.set_relation(f'{user2}_friend', user1)
    return render(request, 'user/accept_friend.html', data)


def reject(request):
    data,user1,user2 = for_two_users(request)
    postgre_tool.reject_friendship(user1, user2)
    redis_tool.del_relation(f'{user1}_incoming', user2)
    redis_tool.set_relation(f'{user1}_follower', user2)
    return render(request, 'user/reject_friend.html', data)


def delete(request):
    data,user1,user2 = for_two_users(request)
    postgre_tool.reject_friendship(user1, user2)
    redis_tool.del_relation(f'{user2}_friend', user2)
    redis_tool.del_relation(f'{user2}_friend', user1)
    redis_tool.set_relation(f'{user1}_follower', user2)
    redis_tool.set_relation(f'{user2}_outgoing', user1)
    return render(request, 'user/delete_friend.html', data)


def outgoing(request):
    data, user = for_user(request)
    result = redis_tool.get_data(f'{user}_outgoing', -1)
    print(result)
    return render(request, 'user/outgoing_info.html', data)


def incoming(request):
    data, user = for_user(request)
    result = redis_tool.get_data(f'{user}_incoming', -1)
    return render(request, 'user/incoming_info.html', data)


def friend(request):
    user = for_user(request)
    result = redis_tool.get_data(f'{user}_friend', -1)
    form = RelationsForm()
    data = {
        'form': form
    }
    return render(request, 'user/friend_info.html', data)


def status(request):
    return render(request, 'user/status_info.html')
