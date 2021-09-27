from django.core.paginator import Paginator
from django.db import models
from django_quill.fields import QuillField
from apps.user.models import UserInfo


# 学期表
class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('学期名称', max_length=128)
    # user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, related_name='user_semesters', on_delete=models.CASCADE)
    created = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '学期表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    @property
    def subjects(self):
        return self.semester_subjects.all

    @property
    def subjects_page(self):
        paginator = Paginator(self.subjects(), per_page=5)
        page = paginator.page(1)
        return page


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('科目名称', max_length=128)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    # user = models.ForeignKey(UserInfo,  on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, related_name='user_subjects', on_delete=models.CASCADE)
    # semester = models.ForeignKey(Semester, on_delete=models.CASCADE,)
    semester = models.ForeignKey(Semester, related_name='semester_subjects', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '科目表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    @property
    def topics(self):
        return self.subject_topics.all

    @property
    def topics_page(self):
        paginator = Paginator(self.topics(), per_page=5)
        page = paginator.page(1)
        return page


# 话题表
class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('话题名称', max_length=128)
    content = QuillField('富文本内容')
    clicks = models.IntegerField('点击次数', default=0)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    # user = models.ForeignKey(UserInfo,  on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, related_name='user_topics', on_delete=models.CASCADE)
    # subject = models.ForeignKey(Subject,  on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='subject_topics', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '话题表'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name

    @property
    def comments(self):
        return self.topic_comments.all

    @property
    def subjects_page(self):
        paginator = Paginator(self.comments(), per_page=5)
        page = paginator.page(1)
        return page


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = QuillField('评论内容')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    # user = models.ForeignKey(UserInfo,  on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, related_name='user_comments', on_delete=models.CASCADE)
    # topic = models.ForeignKey(Topic,  on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='topic_comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论表'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f'{self.created}'

