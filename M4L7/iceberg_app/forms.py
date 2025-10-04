from django import forms
from .models import WorkSpace, Board, Comment, Task, UserInvite
class WorkspaceCreationForm(forms.ModelForm):
    class Meta:
        model = WorkSpace
        fields = ['name']

class BoardCreationForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name']

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['board']

class UserInviteForm(forms.ModelForm):
    class Meta:
        model = UserInvite
        fields = ['workspace', 'recipient']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['workspace'].queryset = WorkSpace.objects.filter(owner=user)

