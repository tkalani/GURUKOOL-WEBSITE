from django.shortcuts import render, HttpResponse, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view

from Professor.models import Course, CourseProfessor, Quiz, QuizOptions
from Doubt.models import Doubt, Comment
from .serializers import CourseSerializer, DoubtSerializer, CommentSerializer, QuizOptionsSerializer
from Student.models import CourseStudent, StudentProfile
from django.views.decorators.csrf import csrf_exempt
from django.views import View

import json
# import requests
import traceback

student_group = 'Student'
prof_group = 'Professor'
login_url = 'UserAuth:login'

def group_required(*group_names, login_url=None):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url=login_url)


class CourseList(APIView):
    serializer_class = CourseSerializer
    def get(self, request, type, menu, format=None):    #get courses stduent is registed for
        if type == 'student':
            if menu == 'quiz':
                courses = CourseStudent.objects.all()
        elif type == 'professor':
            print ("request", request, request.user.id)

            courses = CourseProfessor.objects.filter(professor__user__user__id=request.user.id)
            print (courses, "courses")

        else:
            return Response(status=500)
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)


class CourseDoubt(APIView):
    serializer_class = DoubtSerializer

    def get(self, request, course_id, format=None):         #doubts in a course
        doubts = Doubt.objects.filter(course__id=course_id)
        serializer = self.serializer_class(doubts, many=True)
        return Response(serializer.data)


class DoubtCreate(APIView):
    serializer_class = DoubtSerializer

    def get(self, request, format=None):        #doubts of a student
        doubts = Doubt.objects.filter(student__user__user__username=request.user.username)
        serializer = self.serializer_class(doubts, many=True)
        # print(serializer.data)
        return Response(serializer.data)

    @method_decorator(group_required(student_group, login_url=login_url))
    def post(self, request, format=None):       #code, title, description
        try:
            username = request.user.username
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                student = StudentProfile.objects.get(user__user__id=request.user.id)
                serializer.save(student=student)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)

    def delete(self, request, format=None):         #id
        try:
            doubt_id = request.data.get('id')
            if doubt_id is None:
                return Response(status=status.HTTP_206_PARTIAL_CONTENT)
            doubt = Doubt.objects.get(id = doubt_id)
            if request.user.id == doubt.student.user.user.id:
                doubt.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)

    def put(self, request, format=None):        #id, title|description
        try:
            doubt_id = request.data.get('id')
            if doubt_id is None:
                return Response(status=status.HTTP_206_PARTIAL_CONTENT)
            doubt = Doubt.objects.get(id = doubt_id)
            if request.user.id == doubt.student.user.user.id:
                serializer = self.serializer_class(doubt, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)


class CommentCreate(APIView):
    serializer_class = CommentSerializer

    def get(self, request, doubt_id):
        # doubt_id = self.kwargs['doubt_id']
        comments = Comment.objects.filter(doubt__id=doubt_id)
        serializer=self.serializer_class(comments, many=True)
        return Response(serializer.data)

    def post(self, request, doubt_id, format=None):       #text
        try:
            # doubt_id = self.kwargs['doubt_id']
            user_id = request.user.id
            serializer = self.serializer_class(data=request.data)
            print(serializer)
            if serializer.is_valid():
                user = User.objects.get(id=user_id)
                doubt=Doubt.objects.get(id=doubt_id)
                serializer.save(user=user, doubt=doubt)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)

    def put(self, request, doubt_id, format=None):        #id, text
        try:
            comment = Comment.objects.get(id=request.data.get('id'))
            if request.user.id == comment.user.id:
                serializer = self.serializer_class(comment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)

    def delete(self, request, doubt_id, format=None):         #id
        try:
            comment_id = request.data.get('id')
            if comment_id is None:
                return Response(status=status.HTTP_206_PARTIAL_CONTENT)
            comment = Comment.objects.get(id=comment_id)
            if request.user.id == comment.user.id:
                comment.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)

class CheckQuiz(APIView):
    def get(self, request, quiz_id, course_id):
        print ("checking quiz")
        try:
            check_quiz = get_object_or_404(Quiz, course__id=course_id, unique_quiz_id=quiz_id)
            return JsonResponse({"check":True}, status=200)
        except Exception as e:
            return JsonResponse({"check":False}, status=200)        



class QuizDetails(APIView):
    def get(self, request, quiz_id):
        quiz = Quiz.objects.all()[1]
        questions = quiz.quizquestion_set.all()
        fullQuiz = {}
        value = []
        for question in questions:
            options = question.quizoptions_set.all()
            answers = [{"answer":opt.option, "correct":opt.is_correct, "selected":False} for opt in options]
            value.append({"questionText":question.question,"questionTime":question.time,"questionMarks":question.marks, "answers":answers})
        fullQuiz["questions"] = value
        # print (fullQuiz)
        return JsonResponse(fullQuiz, status=200, safe=False)



'''
class Test(View):
    @method_decorator(csrf_exempt)
    def get(self, request):
        print('get success')
        return HttpResponse("Get success")
    def post(self, request):       #text
        print ("done")
        jsonResponse=json.loads(request.body.decode('utf-8'))
        print(jsonResponse['email'])
        print(jsonResponse['email'])
        return "done"
'''