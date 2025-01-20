from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Attachment
from .forms import TaskForm, PriorityForm, CategoryForm, TagForm, CommentForm

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all()
    attachments = task.attachments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = CommentForm()

    context = {
        'task': task,
        'comments': comments,
        'attachments': attachments,
        'form': form,
    }
    return render(request, 'tasks/task_detail.html', context)


def task_list(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        
        return render(request, 'tasks/task_list.html', {'tasks': tasks})
    else:
        return redirect('login')

#CRUD для задач
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()

            files = request.FILES.getlist('attachments')
            for file in files:
                Attachment.objects.create(task=task, file=file)

            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save()
            form.save_m2m()

            files = request.FILES.getlist('attachments')
            for file in files:
                Attachment.objects.create(task=task, file=file)

            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})
        

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task/task_confirm_delete.html', {'task': task})


#создание тегов, категорий, приоритета
def priority_add(request):
    if request.method == "POST":
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('priority_add')
    else:
        form = PriorityForm()
    return render(request, 'tasks/priority_form.html', {'form': form})


def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_add')
    else:
        form = CategoryForm()
    return render(request, 'tasks/category_form.html', {'form': form})


def tag_add(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_add')
    else:
        form = TagForm()
    return render(request, 'tasks/tag_form.html', {'form': form})
