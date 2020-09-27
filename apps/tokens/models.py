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
  name = models.CharField(max_length=50)
  mobile = models.CharField(max_length=16)
  password = models.CharField(max_length=32)
  

class Exam(models.Model):  
  title = models.CharField(max_length=256)
  total_marks = models.IntegerField()
  duration = models.IntegerField()
  
class Question(models.Model):
  title = models.CharField(max_length=256)
  options = JSONField()
  
  
class UserExam(models.Model):  
  total_qustion = models.IntegerField()
  achieved_marks = models.IntegerField()
  fk_user_id = models.ForeignKey("tokens.User", on_delete=models.CASCADE)
  fk_exam_id = models.ForeignKey("tokens.Exam", on_delete=models.CASCADE)
    STATUS = [
    ('completed', 'Completed'),
    ('done', 'Done),
    ('windows', 'Windows App'),
    ('web', 'Web App')
  ]
  status = models.CharField(choices=STATUS, max_length=50)
  

class UserExamDetail(models.Model):
  fk_userexam_id = models.ForeignKey("tokens.UserExam", on_delete=models.CASCADE)
  fk_question_id = models.ForeignKey("tokens.Question", on_delete=models.CASCADE)
  correct = models.BooleanField()
  answered = models.CharField(max_length=2)