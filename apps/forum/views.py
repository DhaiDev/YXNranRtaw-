from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from apps.forum.forms import Form
from apps.forum.models import Semester, Subject, Topic, Comment
from apps.user.models import UserInfo
from apps.user.views import check_login


def create_content_paginator(request, queryset, page_size=5):
    page = request.GET.get('page')
    paginator = Paginator(queryset, page_size)
    try:
        content = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        content = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        content = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不正常
        content = paginator.page(1)
    content.now_page = page
    return content


def check_result(request, result):
    username = request.session.get('name')
    if not result:
        return render(
            request,
            '404.html',
            context={'username': username}
        )
    return username


class IndexView(View):  # 即 SemesterView
    # 所有的 学期  和 所有的科目
    # 所有的学期 是否翻页
    # 所有的 科目 是否 翻页
    # 点击其中的 一个科目 即跳到 科目页面
    def get(self, request, *args, **kwargs):
        username = request.session.get('name')
        semesters = Semester.objects.all()
        content = create_content_paginator(request, queryset=semesters, page_size=5)

        return render(
            request, 'index.html',
            context={'username': username, 'content': content}
        )

    def post(self, request, *args, **kwargs):
        username = request.session.get('name')
        semesters = Semester.objects.all()
        content = create_content_paginator(request, queryset=semesters, page_size=5)

        return render(
            request, 'index.html',
            context={'username': username, 'content': content}
        )


class SemesterView(View):
    # 其中的 一个科目
    # 科目页面 即 当前科目的所有话题 (话题分页)
    def get(self, request, *args, **kwargs):
        sid = request.GET.get('id')
        # todo
        subject = Subject.objects.filter(id=sid).first()
        username = check_result(request, subject)
        if subject:
            topics = subject.topics()
            content = create_content_paginator(request, queryset=topics, page_size=15)
            content.subject = subject
            return render(
                request,
                'semester.html',
                context={'username': username, 'content': content}
            )
        else:
            return render(request, '404.html', context={'error': '??????????????'})


class TopicView(View):
    # 其中的 一个话题
    def get(self, request, *args, **kwargs):
        tid = request.GET.get('id')

        topic = Topic.objects.filter(id=tid).first()
        topic.clicks += 1
        topic.save()
        username = check_result(request, topic)
        comments = topic.comments()
        content = create_content_paginator(request, queryset=comments, page_size=5)
        content.topic = topic
        return render(
            request,
            'topic.html',
            context={'username': username, 'content': content, 'form': Form}
        )

    @check_login
    def post(self, request, *args, **kwargs):
        topic_id = request.POST.get('topic', '')
        content = request.POST.get('content')
        topic = Topic.objects.filter(id=topic_id).first()
        username = check_result(request, topic)
        if content:
            user = UserInfo.objects.filter(username=username).first()
            comment = Comment(user=user, topic_id=topic_id, content=content)
            comment.save()
        comments = topic.comments()
        content = create_content_paginator(request, queryset=comments, page_size=5)
        content.topic = topic
        return render(
            request,
            'topic.html',
            context={'username': username, 'content': content, 'form': Form}
        )


class PublicView(View):
    @check_login
    def get(self, request, pid, *args, **kwargs):
        subject = Subject.objects.filter(id=pid).first()
        # semester = subject.semester
        username = request.session.get('name')
        return render(
            request,
            'public.html',
            context={'username': username, 'form': Form, 'content': {'subject': subject}}
        )

    @check_login
    def post(self, request, pid, *args, **kwargs):
        subject = Subject.objects.filter(id=pid).first()
        username = request.session.get('name')
        user = UserInfo.objects.filter(username=username).first()
        name = request.POST.get('title')
        content = request.POST.get('content')
        semester_id = request.POST.get('semester_id')
        if pid and name and content and semester_id:

            try:
                topic = Topic(name=name, content=content, subject_id=pid,user=user)
                topic.save()
                red = redirect(f'/topic/?id={topic.id}')

            except Exception as E:
                print(E)
                red = redirect(f'/404/')
            return red

        return render(
            request,
            'public.html',
            context={'username': username, 'form': Form, 'content': {'subject': subject}}

        )


class SearchView(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get('name')
        search_value = request.GET.get('value')
        # contents = []
        # if '||' in search_value:
        #     search_values = search_value.split('||')
        topics = Topic.objects.filter(name__contains=search_value).all()
        content = create_content_paginator(request, queryset=topics, page_size=15)
        content.search_value = search_value

        return render(
            request, 'search.html',
            context={'username': username, 'content': content}
        )

    # def post(self, request, *args, **kwargs):
    #     username = request.session.get('name')
    #     search_value = request.POST.get('value')
    #     return render(
    #         request, 'search.html',
    #         context={'username': username, 'content': 'content'}
    #     )


def Error404(request):
    username = request.session.get('name')
    return render(request,'404.html',context={'username': username})