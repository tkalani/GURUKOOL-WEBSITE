from rest_framework import serializers
from django.shortcuts import get_object_or_404

from Student.models import CourseStudent, StudentProfile
from Professor.models import Course
from Doubt.models import Doubt


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='course.name')
    code = serializers.CharField(source='course.code')

    class Meta:
        model = CourseStudent
        fields = ("id", "name", "code")

        read_only_fields = ['id']


class DoubtSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='student.user.user.username', read_only=True)
    code = serializers.CharField(source='course.code')
    last_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Doubt
        fields = ("creator", "id", "code", "title", "description", "last_updated")

    def create(self, validated_data):
        # user = get_object_or_404(StudentProfile, user__user__username=self.context['username'])
        code = validated_data.pop('course')['code']
        course = get_object_or_404(Course, code=code)
        return Doubt.objects.create( course=course, **validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
