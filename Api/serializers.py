from rest_framework import serializers
from django.shortcuts import get_object_or_404

from Student.models import CourseStudent, StudentProfile
from Professor.models import Course
from Doubt.models import Doubt, Comment


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='course.name')
    code = serializers.CharField(source='course.code')
    course_id = serializers.IntegerField(source='course.id')

    class Meta:
        model = CourseStudent
        fields = ("id", "course_id", "name", "code")

        read_only_fields = ['id']


class DoubtSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='student.user.user.username', read_only=True)
    code = serializers.CharField(source='course.code')
    last_updated = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

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


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)
    doubt_title = serializers.CharField(source='doubt.title', read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ("doubt_title", "id", "username", "first_name", "last_name", "text", "last_updated")

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
