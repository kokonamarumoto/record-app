from django.db import models

from django.contrib.auth.models import User
# Create your models here.



class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="日付")
    title = models.CharField(verbose_name="日記タイトル",max_length=100)     # 日記タイトル
    content = models.TextField(verbose_name="日記内容")                 # 日記内容

    image = models.ImageField(verbose_name="写真",upload_to='images/', null=True, blank=True)
    location = models.CharField(verbose_name="場所",max_length=100, blank=True)  # 場所
    favorite = models.BooleanField(verbose_name="お気に入り登録",default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return f"{self.date} - {self.title}"

class StudyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="日付")
    memo = models.TextField(verbose_name="メモ",blank=True) # 学習内容など
  
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorite = models.BooleanField(default=False, verbose_name="お気に入り登録")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.date}の学習記録"

class StudyRecordItem(models.Model):
    record = models.ForeignKey(StudyRecord, on_delete=models.CASCADE, related_name='items')
    subject = models.CharField(verbose_name="カテゴリー",max_length=100)
    study_time = models.PositiveIntegerField(verbose_name="学習時間(分)",help_text="分")

    def __str__(self):
        return f"{self.subject} {self.study_time}分"
