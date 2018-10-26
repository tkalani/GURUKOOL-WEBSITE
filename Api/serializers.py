from rest_framework import serializers
from django.shortcuts import get_object_or_404

from Student.models import CourseStudent, StudentProfile, QuizResult
from Professor.models import Course, ProfessorProfile, Quiz, QuizOptions, QuizQuestion, ConductQuiz
from Doubt.models import Doubt, Comment
from Meeting.models import Meeting


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


class MeetingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='student.user.user.username', read_only=True)
    first_name = serializers.CharField(source='student.user.user.first_name', read_only=True)
    last_name = serializers.CharField(source='student.user.user.last_name', read_only=True)
    professor = serializers.CharField(source='professor.user.user.username')
    created_time = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Meeting
        fields = ("username", "first_name", "last_name", "professor", "id", "title", "body", "status", "prof_response", "created_time")

    def create(self, validated_data):
        professor_username = validated_data.pop('professor')['user']['user']['username']
        professor = get_object_or_404(ProfessorProfile, user__user__username=professor_username)
        return Meeting.objects.create(professor=professor, **validated_data)

    def update(self, instance, validated_data):
        # instance.title = validated_data.get('title', instance.title)
        # instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.prof_response = validated_data.get('prof_response', instance.prof_response)
        instance.save()
        return instance

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class QuizQuestionSerializer(serializers.ModelSerializer):
    # quiz = QuizSerializer(many=False)
    class Meta:
        model = QuizQuestion
        fields = '__all__'

class QuizOptionsSerializer(serializers.ModelSerializer):
    # quiz = QuizSerializer(many=False)
    # question = QuizQuestionSerializer(many=False)
    class Meta:
        model = QuizOptions
        fields = '__all__'

class ConductQuizSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(many=False)
    class Meta:
        model = ConductQuiz
        fields = ('quiz', 'unique_quiz_id', 'active', 'conduction_date')

class QuizResultSerializer(serializers.ModelSerializer):
    conduct_quiz = ConductQuizSerializer(many=False)
    class Meta:
        model = QuizResult
        fields = ("student", "conduct_quiz", "marks_obtained")