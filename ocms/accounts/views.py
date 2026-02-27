from django.shortcuts import render
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import traceback

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    if request.method == 'GET':
        return Response(UserSerializer(user).data)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        user.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@csrf_exempt
@api_view(['POST', 'OPTIONS'])
@permission_classes([AllowAny])
def custom_token_obtain(request):
    if request.method == 'OPTIONS':
        return Response(status=200)

    try:
        raw_email = request.data.get('email')
        password = request.data.get('password')
        email = raw_email.lower() if raw_email else None
        
        print(f"DEBUG: Login attempt for {email} (raw: {raw_email})")
        
        # Try multiple authentication patterns
        user = authenticate(username=email, password=password)
        if not user:
            user = authenticate(email=email, password=password)
        if not user:
            user = authenticate(username=raw_email, password=password)
        if not user:
            user = authenticate(email=raw_email, password=password)

        if user:
            print(f"DEBUG: Auth SUCCESS for {user.email}")
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            print(f"DEBUG: Auth FAILED for {email}")
            # Additional DB check for debugging
            try:
                user_obj = User.objects.filter(email__iexact=email).first()
                if user_obj:
                    print(f"DEBUG: User exists but auth failed. Active: {user_obj.is_active}, Hashed: {user_obj.password.startswith('pbkdf2_sha256$')}")
                else:
                    print(f"DEBUG: User does not exist in database.")
            except:
                pass
            return Response({"detail": "No active account found with the given credentials"}, status=401)
    except Exception as e:
        with open('traceback.txt', 'w') as f:
            f.write(traceback.format_exc())
        return Response({"error": str(e)}, status=500)