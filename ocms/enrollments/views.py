from .models import *
from .serializers import *
from courses.models import Course, Lecture
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments(request):
    enrollments = Enrollment.objects.filter(student_id=request.user).select_related('course_id')
    data = []
    for en in enrollments:
        total_lectures = Lecture.objects.filter(module_id__course_id=en.course_id).count()
        completed_lectures = LectureProgress.objects.filter(enrollment_id=en, completed=True).count()
        data.append({
            "id": en.id,
            "course": {
                "id": en.course_id.id,
                "title": en.course_id.title,
                "description": en.course_id.description,
            },
            "status": en.status,
            "total_lectures": total_lectures,
            "completed_lectures": completed_lectures
        })
    return Response(data)

@api_view(['GET', 'POST'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def enrollment_list(request):
    if request.method == 'GET':
        data = Enrollment.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(data, request)
        serializer = EnrollmentSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def enrollment_detail(request, id):
    try:
        obj = Enrollment.objects.get(id=id)
    except:
        return Response({'error': 'Enrollment not found'}, status=404)
    if request.method == 'GET':
        return Response(EnrollmentSerializer(obj).data)
    if request.method == 'PUT':
        serializer = EnrollmentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = EnrollmentSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'POST'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def lectureprogress_list(request):
    if request.method == 'GET':
        data = LectureProgress.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(data, request)
        serializer = LectureProgressSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = LectureProgressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def lectureprogress_detail(request, id):
    try:
        obj = LectureProgress.objects.get(id=id)
    except:
        return Response({'error': 'Progress not found'}, status=404)
    if request.method == 'GET':
        return Response(LectureProgressSerializer(obj).data)
    if request.method == 'PUT':
        serializer = LectureProgressSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = LectureProgressSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)