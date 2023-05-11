from django.shortcuts import render
from .forms import UserForm, TwoUsersForm
from .functions_postgres import PostgresTools

postgre_tool = PostgresTools()


def for_user(request):
    submitbutton = request.POST.get("submit")
    username = ''
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
    form = UserForm()
    data = {
        'form': form
    }
    return data, username


def for_two_users(request):
    submitbutton = request.POST.get("submit")
    user1 = ''
    user2 = ''
    if request.method == 'POST':
        form = TwoUsersForm(request.POST or None)
        if form.is_valid():
            user1 = form.cleaned_data.get('user1')
            user2 = form.cleaned_data.get('user2')
    form = TwoUsersForm()
    data = {
        'form': form
    }
    return data, user1, user2


def hello(request):
    return render(request, 'user/hello.html')


def create(request):
    data, username = for_user(request)
    postgre_tool.create_user(username)
    return render(request, 'user/create_user.html', data)


def send(request):
    data, user1, user2 = for_two_users(request)
    postgre_tool.send_friendship(user1, user2)
    return render(request, 'user/send_friend.html', data)


def accept(request):
    data, user1, user2 = for_two_users(request)
    postgre_tool.accept_friendship(user1, user2)
    return render(request, 'user/accept_friend.html', data)


def reject(request):
    data, user1, user2 = for_two_users(request)
    postgre_tool.reject_friendship(user1, user2)
    return render(request, 'user/reject_friend.html', data)


def delete(request):
    data, user1, user2 = for_two_users(request)
    postgre_tool.delete_friendship(user1, user2)
    return render(request, 'user/delete_friend.html', data)

def users(request):
    submitbutton = request.GET.get("submit")
    if request.method == 'GET':
        if request.GET:
            result = postgre_tool.get_users()
            return render(request, 'user/info_requests.html', {'result': result})
    return render(request, 'user/show_users.html')

def relations(request):
    submitbutton = request.GET.get("submit")
    if request.method == 'GET':
        if request.GET:
            result = postgre_tool.get_relations()
            return render(request, 'user/info_requests.html', {'result': result})
    return render(request, 'user/show_relations.html')

def outgoing(request):
    submitbutton = request.POST.get("submit")
    form = UserForm()
    data = {
        'form': form
    }
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            result = postgre_tool.get_outgoing_request(username)
            return render(request, 'user/info_requests.html', {'result': result})
    return render(request, 'user/outgoing_info.html', data)


def incoming(request):
    submitbutton = request.POST.get("submit")
    form = UserForm()
    data = {
        'form': form
    }
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            result = postgre_tool.get_incoming_request(username)
            return render(request, 'user/info_requests.html', {'result': result})
    return render(request, 'user/incoming_info.html', data)


def friend(request):
    submitbutton = request.POST.get("submit")
    form = UserForm()
    data = {
        'form': form
    }
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            result = postgre_tool.get_friends(username)
            return render(request, 'user/info_requests.html', {'result': result})
    return render(request, 'user/friend_info.html', data)


def follower(request):
    submitbutton = request.POST.get("submit")
    form = UserForm()
    data = {
        'form': form
    }
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            result = postgre_tool.get_followers(username)
            return render(request, 'user/info_requests.html', {'result': result})
    return render(request, 'user/friend_info.html', data)


def status(request):
    submitbutton = request.POST.get("submit")
    form = TwoUsersForm()
    data = {
        'form': form
    }
    if request.method == 'POST':
        form = TwoUsersForm(request.POST or None)
        if form.is_valid():
            user1 = form.cleaned_data.get('user1')
            user2 = form.cleaned_data.get('user2')
            result = postgre_tool.get_status(user1, user2)
            return render(request, 'user/info_requests.html', {'result': result})
    return render(request, 'user/status_info.html', data)
