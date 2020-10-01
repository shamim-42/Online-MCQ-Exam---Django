from django.db import models
from django_mysql.models import JSONField

# Create your models here.
class Token(models.Model):
  APP = [
    ('android', 'Android App'),
    ('ios', 'IOS App'),
    ('windows', 'Windows App'),
    ('web', 'Web App')
  ]
  appname = models.CharField(max_length=16, choices=APP, null=True)
  userId = models.CharField(max_length=8, verbose_name="User Id")
  device_token = models.CharField(max_length=512, verbose_name="Device Token")
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Created At')

  # class Meta:


class User(models.Model):  
  name = models.CharField(max_length=50, null=True)
  mobile = models.CharField(max_length=16)
  password = models.CharField(max_length=32)
  

class Exam(models.Model):  
  title = models.CharField(max_length=256, null=True)
  total_marks = models.IntegerField(null=True)
  duration = models.IntegerField(null=True)
  
class Question(models.Model):
  title = models.CharField(max_length=256, null=True)
  options = JSONField(null=True)
  correct_option = models.CharField(max_length=16, null=True)
  marks = models.IntegerField(null=True)  
  fk_exam = models.ForeignKey("tokens.Exam", on_delete=models.CASCADE, null=True)
  
class UserExam(models.Model):
  total_question = models.IntegerField(null=True)
  achieved_marks = models.IntegerField(null=True)
  fk_user = models.ForeignKey("tokens.User", on_delete=models.CASCADE, null=True)
  fk_exam = models.ForeignKey("tokens.Exam", on_delete=models.CASCADE, null=True)
  STATUS = [
    ('completed', 'Completed'),
    ('done', 'Done')
  ]
  status = models.CharField(choices=STATUS, max_length=50, null=True)

  

class UserExamDetail(models.Model):
  fk_userexam = models.ForeignKey("tokens.UserExam", on_delete=models.CASCADE, null=True)
  fk_question = models.ForeignKey("tokens.Question", on_delete=models.CASCADE, null=True)
  correct = models.BooleanField(null=True)
  answered = models.CharField(max_length=2)