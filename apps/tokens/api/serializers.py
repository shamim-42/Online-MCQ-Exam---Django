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

class UserExam(ModelSerializer):    
    # seller_user_id = serializers.CharField(required=False)
    class Meta:
        model = UserExam        
        fields = '__all__'

class UserExamDetail(ModelSerializer):    
    # seller_user_id = serializers.CharField(required=False)
    class Meta:
        model = UserExamDetail        
        fields = '__all__'

