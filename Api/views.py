from django.shortcuts import render, HttpResponse, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from django.db import connection 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view

from Professor.models import Course, CourseProfessor, Quiz, QuizOptions, ConductQuiz
from Doubt.models import Doubt, Comment
from Meeting.models import Meeting
from UserAuth.models import StudentAuthProfile
from .serializers import CourseSerializer, DoubtSerializer, CommentSerializer, QuizOptionsSerializer, MeetingSerializer, QuizResultSerializer
from Student.models import CourseStudent, StudentProfile, QuizResult, QuizQuestion, QuestionWiseResult
from django.views.decorators.csrf import csrf_exempt
from django.views import View

import json
# import requests
import traceback

student_group = 'Student'
prof_group = 'Professor'
login_url = 'UserAuth:login'

def group_required(*group_names, login_url=None):
    ''' checks group requirement whwther the user is student or professor
        Takes group name as input and login url
        returns status if user passes or not
    '''
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url=login_url)


def CallingStoredProcedure(request):
    if request.method == 'GET':
        cur = connection.cursor()
        cur.callproc('procedure_example_2', [2,])  
        # grab the results  
        results = cur.fetchall()  
        cur.close() 
        print ("results", results)
        return HttpResponse("Procedure Call Success") 



class CourseList(APIView):
    serializer_class = CourseSerializer
    def get(self, request, type, menu, email,format=None):
        '''
        get Courses Student is registered for
        takes input type,menu
        returns students courses in json format
    '''
        if type == 'student':
            if menu == 'quiz':
                courses = CourseStudent.objects.filter(student__user__email_address=email)
                print (courses)
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

    def get(self, request, course_id, format=None):
        '''
        get Student Doubts
        takes input request method,course_id
        returns students doubts in json format
    '''
        doubts = Doubt.objects.filter(course__id=course_id)
        serializer = self.serializer_class(doubts, many=True)
        return Response(serializer.data)


class DoubtCreate(APIView):
    serializer_class = DoubtSerializer
    def get(self, request, course_id, email, format=None):        #doubts of a student
        # can't use request in mobile app
        #doubts = Doubt.objects.filter(student__user__user__username=request.user.username)
        course = get_object_or_404(Course, id=course_id)
        print(course, course.name, course.id)
        doubts = Doubt.objects.filter(course__id=course_id, student__user__email_address=email)        
        serializer = self.serializer_class(doubts, many=True)

        return Response(serializer.data)

    @method_decorator(csrf_exempt)
    # @method_decorator(group_required(student_group, login_url=login_url))
    def post(self, request, course_id, email, format=None):       #code, title, description
        try:
            body = json.loads(request.body.decode('utf-8'))
            student = StudentProfile.objects.get(user__email_address=body['email'])
            print (student)
            Doubt(student=student, course=get_object_or_404(Course, id=course_id), title=body['data']['doubt_title'], description=body['data']['doubt_description']).save()
            # serializer.save(student=student)
            return JsonResponse(True, status=200, safe=False)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print (e)
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
    '''
        Creates a comment,delete a comment api
        takes input request method,doubt_id
        Returns http response fr successful operation
    '''
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


class MeetingManage(APIView):
    '''
        Manages a meeting. Meeting Request Generation
        Takes input request method,type
        Returns corresponding http response on successful creation
    '''
    serializer_class = MeetingSerializer

    def get(self, request, type, format=None):
        if type == 'student':
            meetings = Meeting.objects.filter(student__user__user__id=request.user.id)
        elif type == 'professor':
            meetings = Meeting.objects.filter(professor__user__user__id=request.user.id)
        else:
            return Response(status=500)
        serializer = self.serializer_class(meetings, many=True)
        return Response(serializer.data)

    def post(self, request, type, format=None):     #professor(username),title,body,status,prof_response
        try:
            if type == 'professor':
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                student = StudentProfile.objects.get(user__user__id=request.user.id)
                serializer.save(student=student)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)

    def put(self, request, type, format=None):   #id, status|prof_response
        try:
            if type == 'student':
                return Response(status=status.HTTP_400_BAD_REQUEST)

            meeting = Meeting.objects.get(id=request.data.get('id'))
            if meeting.professor.user.user.id == request.user.id:
                serializer = self.serializer_class(meeting, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)



class CheckQuiz(APIView):
    '''
        API for check Quiz on quiz id,course id
        Takes input, course_id,email,quiz_id
        Returns the quiz status if quiz is completed, quiz id is valid or not
    '''
    def get(self, request, quiz_id, course_id, email):
        print ("checking quiz")
        try:
            check_quiz = get_object_or_404(ConductQuiz, quiz__course__id=course_id, unique_quiz_id=quiz_id, active=True)
            print (email, quiz_id)
            print(QuizResult.objects.filter(student__user__email_address=email, conduct_quiz=check_quiz).count())
            if not(QuizResult.objects.filter(student__user__email_address=email, conduct_quiz=check_quiz).count()):
                return JsonResponse({"check":"Success"}, status=200, safe=False)
            else:
                return JsonResponse({"check":"Completed"}, status=200, safe=False)
        except Exception as e:
            print (e)
            return JsonResponse({"check":"Fail"}, status=500)

class QuizDetails(APIView):
    '''
        Gets Quiz details question wise
        Takes input request method and quiz_id
        Returns the question_id,question_text,question_time,question_marks,answers
    '''
    def get(self, request, quiz_id):
        try:
            quiz = get_object_or_404(ConductQuiz, unique_quiz_id=quiz_id).quiz
            print ("made it prolly")
            questions = quiz.quizquestion_set.all()
            fullQuiz = {}
            value = []
            for question in questions:
                options = question.quizoptions_set.all()
                answers = [{"answer":opt.option, "correct":opt.is_correct, "selected":False} for opt in options]
                value.append({"questionText":question.question, "question_id":question.id, "questionTime":question.time,"questionMarks":question.marks, "answers":answers})
            fullQuiz["questions"] = value
            # print (fullQuiz)
            return JsonResponse(fullQuiz, status=200, safe=False)
        except Exception as e:
            print (e)
            return JsonResponse(False, status=500, safe=False)

class QuizComplete(APIView):
    '''
        Completes the quiz
        takes input request method
        Return json response true or false based on successful operation
    '''
    def post(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            email = body['email']
            quiz_id = body["quiz_id"]
            marks = int(body["marks"])
            stud = get_object_or_404(StudentProfile, user__email_address=email)
            quiz = get_object_or_404(ConductQuiz, unique_quiz_id=quiz_id)
            print (stud, quiz)
            QuizResult(student=stud, conduct_quiz=quiz, marks_obtained=marks, cq_id=quiz_id).save()
            for question in (body['quiz_response']):
                print (question)
                qr = get_object_or_404(QuizResult, student=stud, conduct_quiz=quiz)
                que = get_object_or_404(QuizQuestion, id=question[1])

                '''
                    Populaing data
                '''
                import random
                quiz_options = QuizOptions.objects.filter(question__id=que.id)
                qo = quiz_options[random.randint(0,quiz_options.count()-1)]
                print ("done")
                QuestionWiseResult(quiz_result=qr, question=que, answer=question[0], answer_obtained=qo.option, answer_id=qo.id).save()
            return JsonResponse(True, status=200, safe=False)
        except Exception as e:
            print (e)
            return JsonResponse(False, status=500, safe=False)

class CommentOnDoubt(APIView):
    '''
        Comments in Doubt Thread
        Takes input request method
        Returns json response based on successful operation
    '''
    @method_decorator(csrf_exempt)
    def post(self,request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            Comment(doubt=get_object_or_404(Doubt, id=body['doubt_id']), user=get_object_or_404(User, email=body['email']), text=body['text']).save()
            return JsonResponse(True, status=200, safe=False)
        except Exception as e:
            print (e)
            return JsonResponse(False,status=500)

class Login(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        username = body['json_data']['username']
        password = body['json_data']['password']
        print (username, password)
        try:
            instance = get_object_or_404(StudentAuthProfile, email_address=username)
            print (instance, instance.user.first_name)
            username = instance.user.username
            user = authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({"pass":"Success", "user":username, "name":instance.user.first_name+" "+instance.user.last_name}, status=200, safe=False)
            return JsonResponse("Invalid", status=401, safe=False)
        except Exception as e:
            print (e)
            return body("Wrong Username", status=401, safe=False)

class AllStudentQuiz(APIView):
    serializer_class = QuizResultSerializer

    def get(self, request, course_id, email):
        print ("all student quizzes")
        try:
            results = QuizResult.objects.filter(student__user__email_address=email, conduct_quiz__quiz__course__id=course_id)
            quiz_results = QuizResultSerializer(results, many=True).data
            return JsonResponse(quiz_results, status=200, safe=False)
        except Exception as e:
            print (e)
            return JsonResponse(False, status=500)


class CreateMeeting(APIView):
    serializer_class = MeetingSerializer
    def get(self, request, course_id, email, format=None):        
        meetings = Meeting.objects.filter(student__user__email_address=email)
        serializer = self.serializer_class(meetings, many=True)
        return Response(serializer.data)

    @method_decorator(csrf_exempt)
    def post(self, request, course_id, email, format=None):
        try:
            body = json.loads(request.body.decode('utf-8'))
            print (body)
            student = StudentProfile.objects.get(user__email_address=body['email'])
            professor = get_object_or_404(CourseProfessor, course__id=course_id).professor
            Meeting(student=student, professor=professor, title=body['data']['meeting_title'], body=body['data']['meeting_description']).save()
            return JsonResponse(True, status=200, safe=False)
        except Exception as e:
            print (e)
            print(traceback.format_exc())
            return Response(status=500)
        

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
