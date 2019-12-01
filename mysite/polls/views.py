from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *

"""
質問 "インデックス" ページ -- 最新の質問をいくつか表示
質問 "詳細" ページ -- 結果を表示せず、質問テキストと投票フォームを表示
質問 "結果" ページ -- 特定の質問の結果を表示
投票ページ -- 特定の質問の選択を投票として受付
"""


class IndexView(generic.ListView):
    context_object_name = 'latest_questions'
    template_name = 'polls/index.html'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultslView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': 'You do not select choices'
        }
        return render(
            request,
            'polls/detail.html',
            context
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
