from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

from .forms import WorkspaceCreationForm, BoardCreationForm, TaskCreationForm, UserInviteForm
from .models import WorkSpace, Board, Task


class RegisterView(FormView):
    template_name = 'iceberg_app/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/home')

class LoginView(FormView):
    template_name = 'iceberg_app/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('/home')

class WorkspaceCreationView(LoginRequiredMixin ,FormView):
    template_name = 'iceberg_app/create_workspace.html'
    form_class = WorkspaceCreationForm

    def form_valid(self, form):
        workspace = form.save(commit=False)
        workspace.owner = self.request.user
        workspace.save()
        workspace.members.add(self.request.user)
        return redirect('/home')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/register')

@login_required
def home_view(request):

    workspaces = request.user.member_workspaces.all()

    context = {}

    context['workspaces'] = workspaces

    return render(request, 'iceberg_app/home.html', context)

@login_required
def workspace_view(request, id):
    workspace = get_object_or_404(WorkSpace, id=id)

    if request.user not in workspace.members.all():
        return redirect('/home')

    context = {}

    context['members'] = workspace.members.all()

    context['workspace'] = workspace

    context['boards'] = Board.objects.filter(workspace=workspace)


    return render(request, 'iceberg_app/workspace.html', context)

@login_required
def delete_workspace_view(request, id):
    workspace = get_object_or_404(WorkSpace, id=id)

    if request.user == workspace.owner:
        workspace.delete()
        return redirect('/home')
    else:
        return redirect('/home')


@login_required
def create_board_view(request, id):
    workspace = get_object_or_404(WorkSpace, id=id)

    if request.user != workspace.owner:
        return redirect('/home')

    context = {}

    if request.method == 'POST':
        form = BoardCreationForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.workspace = workspace
            board.save()
            return redirect(f'/workspace/{id}')
    else:
        form = BoardCreationForm()

    context['form'] = form
    context['workspace'] = workspace
    return render(request, 'iceberg_app/create_board.html', context)

@login_required
def delete_board_view(request, board_id, workspace_id):

    workspace = get_object_or_404(WorkSpace, id=workspace_id)
    board = get_object_or_404(Board, id=board_id)

    if request.user != workspace.owner:
        return redirect('/home')

    board.delete()

    return redirect(f'/workspace/{workspace_id}')

@login_required
def create_task_view(request, board_id, workspace_id):

    workspace = get_object_or_404(WorkSpace, id=workspace_id)
    board = get_object_or_404(Board, id=board_id)

    if request.user != workspace.owner:
        return redirect('/home')

    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.board = board
            task.save()
            return redirect(f'/workspace/{workspace_id}')
    else:
        form = TaskCreationForm()

    context = {'form': form}
    context['board'] = board
    context['workspace'] = workspace

    return render(request, 'iceberg_app/create_task.html', context)

@login_required
def task_info_view(request, task_id, workspace_id):

    workspace = get_object_or_404(WorkSpace, id=workspace_id)
    task = get_object_or_404(Task, id=task_id)

    if request.user not in workspace.members.all():
        return redirect('/home')

    context = {'task':task}
    context['workspace'] = workspace

    return render(request, 'iceberg_app/task_info.html', context)

@login_required
def delete_task_view(request, task_id, workspace_id):

    workspace = get_object_or_404(WorkSpace, id=workspace_id)
    task = get_object_or_404(Task, id=task_id)

    if request.user != workspace.owner:
        return redirect('/home')

    task.delete()

    return redirect(f'/workspace/{workspace_id}')

@login_required
def invite_creation_view(request, workspace_id):
    workspace = get_object_or_404(WorkSpace, id=workspace_id)

    if request.user != workspace.owner:
        return redirect('/home')

    if request.method == "POST":
        form = UserInviteForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.sender = request.user
            invite.workspace = workspace
            invite.save()
            return redirect("/workspace", workspace_id=workspace.id)
    else:
        form = UserInviteForm(user=request.user)
        context = {'form':form, 'workspace':workspace}

    return render(request, 'iceberg_app/invite_creation.html', context)








