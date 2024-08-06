from rest_framework import status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response({"success" : True, "message" : "Welcome to the Task management system."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "data" : serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success": False, "error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        return Response({
            'success': True,
            'access': str(refresh.access_token),
            'user': user_serializer.data,
        })
    return Response({"success" : False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# CREATE TASK
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success" : False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_all(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response({"success":True, "data" : serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_by_id(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def task_update(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"success": False, "error":"Task Not Found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "data" : serializer.data})
    return Response({"success": False,"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def task_delete(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"success":False, "message" : "Task Not Found"},status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response({"success" : True, "message" : "Task deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member_all(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"success":True, "data" : serializer.data}, status=status.HTTP_200_OK)
