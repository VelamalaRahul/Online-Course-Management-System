from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import User
from courses.models import Course, Lecture
from enrollments.models import Enrollment
from reviews.models import Review
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([]) # Public access for landing page stats
@cache_page(60 * 5) # Cache for 5 minutes
def analytics(request):
    
    # Basic Stats
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()

    # Advanced Metrics
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    total_duration_hours = (Lecture.objects.aggregate(total=Sum('duration'))['total'] or 0) / 60

    # Growth (Enrollments last 7 days)
    last_week = timezone.now() - timedelta(days=7)
    recent_growth = Enrollment.objects.filter(created_at__gte=last_week).count()

    # Enrollments By Course (Top 5)
    enrollments_qs = Course.objects.annotate(enrollment_count=Count('enrollment')).order_by('-enrollment_count')[:5]
    enrollments_by_course = {c.title: c.enrollment_count for c in enrollments_qs}

    # Review Ratings Distribution (1-5 stars)
    ratings_qs = Review.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
    reviews_by_rating = {r['rating']: r['count'] for r in ratings_qs}

    # Category Distribution
    category_qs = Course.objects.values('category_id__name').annotate(count=Count('id')).order_by('-count')
    category_distribution = {c['category_id__name'] or 'Uncategorized': c['count'] for c in category_qs}

    # Recent Activity (Latest 5 events)
    recent_enrollments_qs = Enrollment.objects.select_related('student_id', 'course_id').order_by('-created_at')[:5]
    enrollment_activity = [{
        "type": "enrollment",
        "user": e.student_id.full_name or e.student_id.username,
        "item": e.course_id.title,
        "time": e.created_at.strftime("%H:%M")
    } for e in recent_enrollments_qs]

    recent_reviews_qs = Review.objects.select_related('student_id', 'course_id').order_by('-created_at')[:5]
    review_activity = [{
        "type": "review",
        "user": r.student_id.full_name or r.student_id.username,
        "item": r.course_id.title,
        "detail": f"{r.rating} stars",
        "time": r.created_at.strftime("%H:%M")
    } for r in recent_reviews_qs]

    recent_activity = sorted(enrollment_activity + review_activity, key=lambda x: x['time'], reverse=True)[:6]

    # Instructor Leaderboard (Top 5)
    instructors = Course.objects.values('instructor_id__full_name').annotate(
        enrollments=Count('enrollment'),
        avg_rating=Avg('review__rating')
    ).order_by('-enrollments')[:5]

    instructor_leaderboard = [{
        "name": i['instructor_id__full_name'] or "Unknown Mentor",
        "enrollments": i['enrollments'],
        "rating": round(i['avg_rating'] or 0, 1)
    } for i in instructors]

    data = {
        "summary": {
            "total_users": total_users,
            "total_courses": total_courses,
            "total_enrollments": total_enrollments,
            "avg_rating": round(avg_rating, 1),
            "total_hours": round(total_duration_hours, 1),
            "recent_growth": recent_growth
        },
        "charts": {
            "enrollments_by_course": enrollments_by_course,
            "reviews_by_rating": reviews_by_rating,
            "category_distribution": category_distribution
        },
        "instructor_leaderboard": instructor_leaderboard,
        "recent_activity": recent_activity
    }
    return Response(data)