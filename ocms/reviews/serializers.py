from rest_framework import serializers
from .models import Review
class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student_id.full_name')
    class Meta:
        model = Review
        fields = ['id', 'student_id', 'student_name', 'course_id', 'rating', 'comment', 'created_at']