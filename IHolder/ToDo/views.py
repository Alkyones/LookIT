from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import TodoList, TodoListItem
from .forms import TodoListForm, TodoListItemForm
# Create your views here.

# creating and displaying existent lists
def UserLists(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TodoListForm(request.POST)
            if form.is_valid():
                new_list = form.save(commit=False)
                new_list.user = request.user
                new_list.save()
                return redirect('/accounts/Todo/')
        else:
            form = TodoListForm()
            todo_lists = TodoList.objects.filter(user=request.user)
        return render(request, 'todo/user_lists.html', {'todo_lists': todo_lists, 'form': form})
    else:
        return redirect('/login/')

def DeleteList(request, listId):
    if request.user.is_authenticated:
        if TodoList.objects.filter(id=listId):
            requested_list = request.user.todolist_set.get(id=listId)
            requested_list.delete()
        return redirect('/accounts/Todo/')


#creating and adding / displaying list items
def ListItems(request, listId):
    if request.user.is_authenticated:
        if request.user.todolist_set.get(id=listId):
            requested_list = request.user.todolist_set.get(id=listId).todolistitem_set.all()
            if request.method == 'POST':
                form = TodoListItemForm(request.POST)
                if form.is_valid():
                    request.user.todolist_set.get(id=listId).todolistitem_set.create(**form.cleaned_data)
                    return redirect(f'/accounts/Todo/{listId}/')
            else:
                form = TodoListItemForm()

    return render(request, 'todo/user_list_item.html', {'todo_items': requested_list, 'form': form, 'listId': listId,})







# update or delete list items
def ListItemsUpdate(request, listId, ItemId):
    
    if request.user.is_authenticated:
        if TodoListItem.objects.filter(id=ItemId):
            requested_item = request.user.todolist_set.get(id=listId).todolistitem_set.get(id=ItemId)
            if requested_item.is_completed:
                requested_item.is_completed = False
            else:
                requested_item.is_completed = True
            requested_item.save()
            return redirect(f'/accounts/Todo/{listId}/')


def ListItemsDelete(request, listId, ItemId):
    if request.user.is_authenticated:
        if TodoListItem.objects.filter(id=ItemId):
            requested_item = request.user.todolist_set.get(id=listId).todolistitem_set.get(id=ItemId)
            requested_item.delete()
            
        return redirect(f'/accounts/Todo/{listId}/')