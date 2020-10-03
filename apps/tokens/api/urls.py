from django.urls import path, include
from rest_framework import routers
from apps.tokens.api import views
mcq_router = routers.DefaultRouter()

mcq_router.register(r'user', views.UserView)
mcq_router.register(r'exam', views.ExamView)
mcq_router.register(r'question', views.QuestionView)
mcq_router.register(r'user-exam', views.UserExamView)
mcq_router.register(r'user-exam-detail', views.UserExamDetailView)


urlpatterns = [
    path('mcq/', include(mcq_router.urls)),
    path('login/', views.LoginView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('answer-evaluation/', views.AnswerEvaluation.as_view()),
]
