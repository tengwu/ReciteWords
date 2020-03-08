from django.db import models

# Create your models here.

from django.db import models

class Word(models.Model):
    spell = models.CharField(max_length=200) #单词拼写
    speak_england = models.CharField(max_length=200, default="") #英式发音
    speak_america = models.CharField(max_length=200, default="") #美式发音
    meaning = models.TextField() #单词的意思，每两个意思之间用&分割，词性中英文意思之间用|分割
    example = models.TextField() #例句，每两个例句之间用&分割，中英文例句之间用|分割

class WordJson(models.Model):
    spell = models.CharField(max_length=200) #单词拼写
    json = models.TextField() #json数据

class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=200)