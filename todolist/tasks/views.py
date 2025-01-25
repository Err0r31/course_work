from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Attachment, Category, Priority, Tag
from .forms import TaskForm, PriorityForm, CategoryForm, TagForm, CommentForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import TaskSerializer, CategorySerializer, PrioritySerializer, TagSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q


def task_list(request):
    if request.user.is_authenticated:
        return render(request, 'tasks/task_list.html') 
    else:
        return redirect('login')


# CRUD для задач
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


# ADD для приоритета, категории и тегов
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


# REST API для задач
# Пагинация для задач
class TaskPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100  


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination  
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category']  
    ordering_fields = ['due_date', 'created_at'] 
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    @action(methods=['GET'], detail=False, url_path='active-tasks')
    def active_tasks(self, request):
        user = request.user
        tasks = self.queryset.filter(Q(status='pending') | Q(status='in_progress'), user=user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    