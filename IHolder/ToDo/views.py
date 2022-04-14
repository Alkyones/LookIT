from django.shortcuts import render, redirect
from .models import TodoList, TodoListItem
from .forms import TodoListForm, TodoListItemForm
# Create your views here.

def UserLists(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TodoListForm(request.POST)
            if form.is_valid():
                new_list = form.save(commit=False)
                new_list.user = request.user
                new_list.save()
                return redirect('/ToDo/lists/')
        else:
            form = TodoListForm()
            todo_lists = TodoList.objects.filter(user=request.user)
        return render(request, 'todo/user_lists.html', {'todo_lists': todo_lists})
    else:
        return redirect('/login/')
