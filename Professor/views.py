from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
import UserAuth.utils as UserAuthutils
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from Doubt.models import *
from Student.models import *
from Meeting.models import *
import hashlib
import time, csv
import datetime
from django.db.models import Count
from .utils import *
from django.http import StreamingHttpResponse

group_name = 'Professor'
login_url = 'UserAuth:login'

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def group_required(*group_names, login_url=None):
    ''' checks group requirement whwther the user is student or professor
        Takes group name as input and login url
        returns status if user passes or not'''
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url=login_url)

''' Login Required
'''
@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def dashboard(request):
    '''
        Loads all the data for the dashboard. Gets active polls, active quizzes, meetings today and doubts overview
        Takes only input GET request whenever the user goes to the dashboard page
        Returns all_doubt_list,poll_list,quiz_list,course_list,meeting_list,active_quiz_list
    '''
    if request.method == 'GET':
        poll_list = Poll.objects.filter(professor__user__user__username=request.user.username).order_by('-id')
        quiz_list = Quiz.objects.filter(professor__user__user__username=request.user.username).order_by('-id')
        course_list = CourseProfessor.objects.filter(professor__user__user__id=request.user.id).order_by('-id')
        meeting_list = (MeetingPlace.objects.filter(meeting__professor__user__user__id=request.user.id, is_ticked=False, meeting_date=time.strftime('%Y-%m-%d'), meeting__status='APPROVED').order_by('meeting_time'))[:1]
        active_poll_list = ConductPoll.objects.filter(poll__professor__user__user__username=request.user.username, active=True).order_by('-id')
        active_quiz_list = ConductQuiz.objects.filter(quiz__professor__user__user__username=request.user.username, active=True).order_by('-id')
        all_doubt_list = []

        for course in course_list:
            for y in Doubt.objects.filter(course__id=course.course.id):
                all_doubt_list.append(y)
        all_doubt_list = sorted(all_doubt_list, key=lambda k: k.last_updated)
        all_doubt_list = all_doubt_list[::-1]
        all_doubt_list = all_doubt_list[:1]

        for quiz in active_quiz_list:
            quiz.submissions = QuizResult.objects.filter(conduct_quiz=quiz).count()
            quiz.total = CourseStudent.objects.filter(course=quiz.quiz.course).count()

        # all_meetings = []
        # meeting_list = (MeetingPlace.objects.filter(meeting__professor__user__user__id=request.user.id, is_ticked=False, meeting_date=time.strftime('%Y-%m-%d'), meeting__status='APPROVED').order_by('meeting_time'))
        # for m in meeting_list:
        #     print(m.meeting_time)
        #     print(datetime.datetime.time(datetime.datetime.now()))
        #     if m.meeting_time >= datetime.datetime.time(datetime.datetime.now()):
        #         print(True)
        #         all_meetings.append(m)
        # print(all_meetings)

        return render(request, 'Professor/dashboard.html', {"all_doubt_list": all_doubt_list, "poll_list": poll_list, "quiz_list": quiz_list, "course_list":course_list, "meeting_list":meeting_list, "active_quiz_list": active_quiz_list, "active_poll_list": active_poll_list})

''' Login Required
'''
@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def create_poll(request):
    '''
        Creates a new Poll. If GET request, then render the web page for adding a poll. If POST request then form submit and adding a poll in database
        Takes only request as input
        if GET request then render the web page for adding a poll. If POST request, add data entries into database and user is redirected to professor
    '''
    if request.method == 'GET':
        course_list = CourseProfessor.objects.filter(professor__user__user__username=request.user.username)
        return render(request, 'Professor/create-poll.html', {'course_list': course_list})

    if request.method == 'POST':
        course = request.POST.get('course')
        title = request.POST.get('title')
        question = request.POST.get('question')
        option_list = request.POST.getlist('poll_options[]')
        try:
            poll_inst = Poll()
            poll_inst.professor = ProfessorProfile.objects.get(user__user__username=request.user.username)
            poll_inst.course = Course.objects.get(id=(CourseProfessor.objects.get(id=course)).course.id)
            poll_inst.title = title
            poll_inst.question = question
            poll_inst.save()
            for option in option_list:
                option_inst = PollOption()
                option_inst.poll = poll_inst
                option_inst.option = option
                option_inst.save()
            messages.success(request, "Successfully created Poll")
            return HttpResponseRedirect(reverse('Professor:all-poll'))
        except Exception as e:
            print(e)
            messages.warning(request, "There was an error creating poll. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:create-poll'))

''' Login Required
'''
@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def show_poll(request, poll_id):
    '''
        This function is for showing a particular poll
        Takes input the poll_id to get a specific poll and request method.
        Retrieves Poll details and render the web page poll-detail.html with variables poll_details,poll_options,is_poll_active.
    '''
    if request.method == 'GET':
        poll_details = Poll.objects.get(id=poll_id)
        poll_options = PollOption.objects.filter(poll__id=poll_id)
        is_poll_active = ConductPoll.objects.filter(active=True, poll__id=poll_id)
        return render(request, 'Professor/poll-detail.html', {"poll_details": poll_details, 'poll_options': poll_options, "is_poll_active": is_poll_active})

''' Login Required
'''
@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def create_quiz(request):
    '''
        Creates a new Quiz. If GET request, then render the web page for adding a quiz. If POST request then form submit and adding a quiz in database
        Takes only request as input
        if GET request then render the web page for adding a poll. If POST request, add data entries into database and user is redirected to professor dashboard
    '''
    if request.method == 'GET':
        course_list = CourseProfessor.objects.filter(professor__user__user__username=request.user.username)
        return render(request, 'Professor/create-quiz.html', {'course_list': course_list})

    if request.method == 'POST':
        try:
            question_option_array = list(map(int, request.POST['question-option'].split(',')))
            quiz = Quiz()
            quiz.professor = ProfessorProfile.objects.get(user__user__username=request.user.username)
            course = CourseProfessor.objects.get(id=int(request.POST['course']))
            quiz.course = Course.objects.get(id=int(course.course.id))
            quiz.title = request.POST['title']
            quiz.description = request.POST['description']
            quiz.max_marks = request.POST['max_marks']
            quiz.pass_marks = request.POST['pass_marks']
            quiz.save()

            question_count = 0
            for i in range(len(question_option_array)):
                if question_option_array[i] != 0:
                    question_count += 1
                    ques_inst = QuizQuestion()
                    ques_inst.quiz = quiz
                    ques_inst.question = request.POST['question_'+str(i+1)]
                    ques_inst.marks = request.POST['marks_'+str(i+1)]
                    ques_inst.time = request.POST['time_'+str(i+1)]
                    ques_inst.save()
                    option_list = request.POST.getlist('poll_options_'+str(i+1)+'[]')
                    for j in range(len(option_list)):
                        opt_inst = QuizOptions()
                        opt_inst.quiz = quiz
                        opt_inst.question = ques_inst
                        opt_inst.option = option_list[j]
                        if request.POST.get('option_checkbox_'+str(i+1)+'_'+str(j+1)) is not None:
                            opt_inst.is_correct = True
                        else:
                            opt_inst.is_correct = False
                        opt_inst.save()
            quiz.no_of_questions = question_count
            quiz.save()
            messages.success(request, "Successfully Created Quiz")
            return HttpResponseRedirect(reverse('Professor:all-quiz'))
        except Exception as e:
            print('error is ', e)
            messages.warning(request, "There was an error creating Quiz. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:create-quiz'))

''' Login Required
'''

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def show_quiz(request, quiz_id):
    '''
    Displays the Quiz
    Take input request method and quiz_id
    Returns quiz_data,is_active_quiz and renders the quiz-detail.html
    '''
    if request.method == 'GET':
        quiz_data = QuizOptions.objects.filter(quiz__id=quiz_id)
        is_quiz_active = ConductQuiz.objects.filter(active=True, quiz__id=quiz_id)
        return render(request, 'Professor/quiz-detail.html', {"quiz_data": quiz_data, "is_quiz_active": is_quiz_active})

''' Login Required
'''

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def conduct_quiz(request, quiz_id):
    '''
        Conducts A Quiz
        Take input request method and quiz_id
        Returns HTTp Response if quiz is successfully conducted or not
    '''
    if request.method == 'GET':
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            unique_quiz_id = str('_'.join(quiz.title.split(' ')))+str(hashlib.sha224((str(quiz.title)+str(time.strftime("%Y-%m-%d"))+str(time.strftime("%H:%i:%s"))+str(quiz.id)).encode('utf-8')).hexdigest())[:5]

            conduct_quiz_inst = ConductQuiz()
            conduct_quiz_inst.quiz = quiz
            conduct_quiz_inst.unique_quiz_id = unique_quiz_id
            conduct_quiz_inst.active = True
            conduct_quiz_inst.save()

            QuizStatistics(quiz_id=conduct_quiz_inst, conduct_quiz_id=unique_quiz_id).save()

            messages.success(request, "Successfully started quiz")
            return HttpResponseRedirect(reverse('Professor:quiz', kwargs={'quiz_id':quiz_id}))
        except Exception as e:
            print(e)
            messages.warning(request, "There was an error conducting Quiz. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:quiz', kwargs={'quiz_id':quiz_id}))

''' Login Required
'''

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def stop_quiz(request, quiz_id):
    '''
        Stops an active quiz
        Take input request method and quiz_id
        Returns HTTp Response if quiz is successfully stopped or not
    '''
    if request.method == 'GET':
        try:
            conduct_quiz_inst = ConductQuiz.objects.get(id=quiz_id)
            conduct_quiz_inst.active = False
            conduct_quiz_inst.save()
            messages.success(request, "Successfully stopped quiz")
            return HttpResponseRedirect(reverse('Professor:conducted-quiz', kwargs={'quiz_id':conduct_quiz_inst.id}))
        except Exception as e:
            print(e)
            messages.warning(request, "There was an error stopping Quiz. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:quiz', kwargs={'quiz_id':conduct_quiz_inst.quiz.id}))

''' Login Required
'''
@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def conduct_poll(request, poll_id):
    '''
        Conducts A Poll
        Take input request method and poll_id
        Returns HTTp Response if poll is successfully conducted or not
    '''
    if request.method == 'GET':
        try:
            poll = Poll.objects.get(id=poll_id)
            unique_poll_id = str('_'.join(poll.title.split(' ')))+str(hashlib.sha224((str(poll.title)+str(time.strftime("%Y-%m-%d"))+str(time.strftime("%H:%i:%s"))+str(poll.id)).encode('utf-8')).hexdigest())[:5]

            conduct_poll_inst = ConductPoll()
            conduct_poll_inst.poll = poll
            conduct_poll_inst.unique_poll_id = unique_poll_id
            conduct_poll_inst.active = True
            conduct_poll_inst.save()

            messages.success(request, "Successfully started Poll")
            return HttpResponseRedirect(reverse('Professor:poll', kwargs={'poll_id':poll_id}))
        except Exception as e:
            print(e)
            messages.warning(request, "There was an error conducting Poll. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:poll', kwargs={'poll_id':poll_id}))

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def stop_poll(request, poll_id):
    '''
        Stops an active Poll
        Take input request method and poll_id
        Returns HTTp Response if poll is successfully stopped or not
    '''
    if request.method == 'GET':
        try:
            conduct_poll_inst = ConductPoll.objects.get(id=poll_id)
            conduct_poll_inst.active = False
            conduct_poll_inst.save()
            messages.success(request, "Successfully stopped Poll")
            return HttpResponseRedirect(reverse('Professor:poll', kwargs={'poll_id':conduct_poll_inst.poll.id}))
        except Exception as e:
            print(e)
            messages.warning(request, "There was an error stopping Poll. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:poll', kwargs={'poll_id':conduct_poll_inst.poll.id}))

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def show_all_polls(request):
    '''
        Shows all polls
        Takes input request method
        Returns all_polls_list,finished_polls_list,active_polls_list and renders the web page
    '''
    if request.method == 'GET':
        try:
            all_poll_list = Poll.objects.filter(professor__user__user__username=request.user.username).order_by('-id')
            finished_poll_list = ConductPoll.objects.filter(poll__professor__user__user__username=request.user.username, active=False).order_by('-id')
            active_poll_list = ConductPoll.objects.filter(poll__professor__user__user__username=request.user.username, active=True).order_by('-id')
            return render(request, 'Professor/polls.html', {"all_poll_list": all_poll_list, "finished_poll_list": finished_poll_list, "active_poll_list": active_poll_list})
        except Exception as e:
            print('error is', e)
            messages.warning(request, "There was an error displaying Polls. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:dashboard'))

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def show_all_quiz(request):
    '''
        Shows all quiz
        Takes input request method
        Returns all_quiz_list,finished_quiz_list,active_quiz_list and renders the web page
    '''
    if request.method == 'GET':
        try:
            all_quiz_list = Quiz.objects.filter(professor__user__user__username=request.user.username).order_by('-id')
            finished_quiz_list = ConductQuiz.objects.filter(quiz__professor__user__user__username=request.user.username, active=False).order_by('-id')
            active_quiz_list = ConductQuiz.objects.filter(quiz__professor__user__user__username=request.user.username, active=True).order_by('-id')

            for quiz in active_quiz_list:
                quiz.submissions = QuizResult.objects.filter(conduct_quiz=quiz).count()
                quiz.total = CourseStudent.objects.filter(course=quiz.quiz.course).count()

            for quiz in finished_quiz_list:
                quiz.submissions = QuizResult.objects.filter(conduct_quiz=quiz).count()
                quiz.total = CourseStudent.objects.filter(course=quiz.quiz.course).count()

            return render(request, 'Professor/quiz.html', {"all_quiz_list": all_quiz_list, "finished_quiz_list": finished_quiz_list, "active_quiz_list": active_quiz_list})
        except Exception as e:
            print('error is', e)
            messages.warning(request, "There was an error displaying Quizzes. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:dashboard'))

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def conducted_poll(request, poll_id):
    if request.method == "GET":
        try:
            conducted_poll = ConductPoll.objects.get(id=poll_id)
            poll_details = Poll.objects.get(id=conducted_poll.poll.id)
            poll_options = PollOption.objects.filter(poll__id=conducted_poll.poll.id)
            return render(request, 'Professor/conducted-poll.html', {"conducted_poll": conducted_poll, "poll_details": poll_details, 'poll_options': poll_options})
        except Exception as e:
            print('error is', e)
            messages.warning(request, "There was an error displaying Quizzes. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:dashboard'))

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def conducted_quiz(request, quiz_id):
    if request.method == 'GET':
        try:
            conducted_quiz = ConductQuiz.objects.get(id=quiz_id)
            quiz_data = QuizOptions.objects.filter(quiz__id=conducted_quiz.quiz.id)
            return render(request, 'Professor/conducted-quiz.html', {"conducted_quiz": conducted_quiz, "quiz_data": quiz_data})
        except Exception as e:
            print('error is', e)
            messages.warning(request, "There was an error displaying Quizzes. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:dashboard'))

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def quiz_result(request, quiz_id):
    if request.method == 'GET':
        try:
            conducted_quiz = ConductQuiz.objects.get(id=quiz_id)
            quiz_statistics = QuizStatistics.objects.get( quiz_id__id=quiz_id)
            quiz_results = QuizResult.objects.filter(conduct_quiz__id=quiz_id).order_by('-marks_obtained')
            return render(request, 'Professor/quiz-result.html', {"conducted_quiz": conducted_quiz,"quiz_statistics":quiz_statistics, "quiz_results": quiz_results})
        except Exception as e:
            print('error is', e)
            messages.warning(request, "There was an error displaying Quizzes. Please Try Again.")
            return HttpResponseRedirect(reverse('Professor:all-quiz'))

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def view_quiz_reponses(request, quiz_id):
    if request.method == 'GET':
        conducted_quiz = ConductQuiz.objects.get(id=quiz_id)
        quiz_statistics = QuizStatistics.objects.get(quiz_id__id=quiz_id)
        question_wise_result = []
        questions = []
        most_correctly_answered, most_correctly_answered_count = [], 0
        most_incorrectly_answered, most_incorrectly_answered_count = [], 0
        most_unattempted_question, most_unattempted_question_count = [], 0
        for question in QuizQuestion.objects.filter(quiz__id=conducted_quiz.quiz.id):
            q_result = QuestionWiseResult.objects.filter(question=question, quiz_result__conduct_quiz=conducted_quiz).values('answer').annotate(total=Count('answer'))
            question_wise_result.append(q_result)
            for r in q_result:
                if r['answer'] == 'correct':
                    if r['total'] > most_correctly_answered_count:
                        most_correctly_answered_count = r['total']
                        most_correctly_answered = [question]
                    elif r['total'] == most_correctly_answered_count:
                        most_correctly_answered.append(question)
                elif r['answer'] == 'wrong':
                    if r['total'] > most_incorrectly_answered_count:
                        most_incorrectly_answered_count = r['total']
                        most_incorrectly_answered = [question]
                    elif r['total'] == most_incorrectly_answered_count:
                        most_incorrectly_answered.append(question)
                elif r['answer'] == 'left':
                    if r['total'] > most_unattempted_question_count:
                        most_unattempted_question_count = r['total']
                        most_unattempted_question = [question]
                    elif r['total'] == most_unattempted_question_count:
                        most_unattempted_question.append(question)
            questions.append(question)
        data = {"question_wise_result":zip(questions, question_wise_result), "conducted_quiz": conducted_quiz,"quiz_statistics":quiz_statistics, "most_correctly_answered": most_correctly_answered, "most_incorrectly_answered": most_incorrectly_answered, "most_unattempted": most_unattempted_question}
        return render(request, 'Professor/quiz-question-responses.html', data)

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def question_wise_result(request):
    conducted_quiz_id = request.GET['conducted_quiz_id']
    question_id = request.GET['question_id']
    val = request.GET['val']
    answer_dict = ['left', 'correct', 'wrong']
    results = QuestionWiseResult.objects.filter(question__id=question_id, quiz_result__conduct_quiz__id=conducted_quiz_id, answer=answer_dict[int(val)])
    return render(request, 'Professor/question-wise-responses.html', {"results": results, "answer": answer_dict[int(val)]})

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def quiz_result_pdf(request, quiz_id):
    if request.method == 'GET':
        conducted_quiz = ConductQuiz.objects.get(id=quiz_id)
        quiz_statistics = QuizStatistics.objects.get( quiz_id__id=quiz_id)
        quiz_results = QuizResult.objects.filter(conduct_quiz__id=quiz_id).order_by('-marks_obtained')
        pdf = render_to_pdf('pdf-templates/quiz-rank-list.html', {"conducted_quiz": conducted_quiz,"quiz_statistics":quiz_statistics, "quiz_results": quiz_results})
        # return HttpResponse(pdf, content_type='application/pdf')
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Quiz-Results-%s.pdf" %(conducted_quiz.unique_quiz_id)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def quiz_result_csv(request, quiz_id):
    if request.method == 'GET':
        conducted_quiz = ConductQuiz.objects.get(id=quiz_id)
        quiz_statistics = QuizStatistics.objects.get( quiz_id__id=quiz_id)
        quiz_results = QuizResult.objects.filter(conduct_quiz__id=quiz_id).order_by('-marks_obtained')
        rows = list()
        rows.append(['Rank', 'Student ID', 'Name', 'Marks', 'Status'])
        for i in range(len(quiz_results)):
            if quiz_results[i].marks_obtained >= conducted_quiz.quiz.pass_marks:
                rows.append([str(i+1), str(quiz_results[i].student.user.user.id), str(quiz_results[i].student.user.user.first_name)+' '+str(quiz_results[i].student.user.user.last_name), str(quiz_results[i].marks_obtained)+'/'+str(conducted_quiz.quiz.max_marks), 'Pass'])
            else:
                rows.append([str(i+1), str(quiz_results[i].student.user.user.id), str(quiz_results[i].student.user.user.first_name)+' '+str(quiz_results[i].student.user.user.last_name), str(quiz_results[i].marks_obtained)+'/'+str(conducted_quiz.quiz.max_marks), 'Fail'])
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename= Quiz-Results-'+str(conducted_quiz.unique_quiz_id)+'.csv'
        return response