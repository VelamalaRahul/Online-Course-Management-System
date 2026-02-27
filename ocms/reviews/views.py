from .models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
@api_view(['GET', 'POST'])
@permission_classes([]) # Public can view reviews
def review_list(request):
    if request.method == 'GET':
        course_id = request.query_params.get('course_id')
        data = Review.objects.all()
        if course_id:
            data = data.filter(course_id=course_id)
        
        paginator = PageNumberPagination()
        paginator.page_size = 100
        paginated = paginator.paginate_queryset(data, request)
        serializer = ReviewSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def review_detail(request, id):
    try:
        obj = Review.objects.get(id=id)
    except:
        return Response({'error': 'Review not found'}, status=404)
    if request.method == 'GET':
        return Response(ReviewSerializer(obj).data)
    if request.method == 'PUT':
        serializer = ReviewSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = ReviewSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)