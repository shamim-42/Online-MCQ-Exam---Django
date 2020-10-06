from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer
)
from apps.tokens.models import *


class UserSerializer(ModelSerializer):
    # seller_user_id = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = '__all__'


class ExamSerializer(ModelSerializer):
    # seller_user_id = serializers.CharField(required=False)
    class Meta:
        model = Exam
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    # seller_user_id = serializers.CharField(required=False)
    class Meta:
        model = Question
        fields = '__all__'


class UserExamSerializer(ModelSerializer):
    # seller_user_id = serializers.CharField(required=False)
    # exam_name = ExtraFieldSerializer()
    class Meta:
        model = UserExam
        read_only_fields = ['exam_name']
        fields = ['id', 'total_question', 'achieved_marks', 'status', 'taken_time', 'fk_user', 'fk_exam']
        # extra_fields = ['exam_name']


class UserExamDetailSerializer(ModelSerializer):
    # seller_user_id = serializers.CharField(required=False)
    class Meta:
        model = UserExamDetail
        fields = '__all__'
