from django.urls import path

from apps.forum.views import IndexView, SemesterView, TopicView, PublicView, SearchView

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('semester/', SemesterView.as_view(), name='semester'),
    path('topic/', TopicView.as_view(), name='topic'),
    path('public/<int:pid>/', PublicView.as_view(), name='public'),
    path('search/', SearchView.as_view(), name='search'),

]


