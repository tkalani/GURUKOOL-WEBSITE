from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from Professor.models import Course
from Doubt.models import Doubt
from .serializers import CourseSerializer, DoubtSerializer
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

    def get(self, request, format=None):
        courses = CourseStudent.objects.filter(student__user__user__username=request.user.username)
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)


class DoubtCreate(APIView):
    serializer_class = DoubtSerializer

    def get(self, request, format=None):
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
