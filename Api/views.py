from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from Professor.models import Course, CourseProfessor
from Doubt.models import Doubt, Comment
from .serializers import CourseSerializer, DoubtSerializer, CommentSerializer
from Student.models import CourseStudent, StudentProfile

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

    def get(self, request, type, format=None):    #get courses stduent is registed for
        if type == 'student':
            courses = CourseStudent.objects.filter(student__user__user__id=request.user.id)
        elif type == 'professor':
            courses = CourseProfessor.objects.filter(professor__user__user__id=request.user.id)
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
